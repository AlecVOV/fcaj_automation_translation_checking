import json
import os
import requests
import boto3
from bs4 import BeautifulSoup
from google.oauth2 import service_account
from googleapiclient.discovery import build
from markdownify import markdownify as md  # THÊM THƯ VIỆN NÀY ĐỂ RENDER BÀI TIẾNG ANH

# Khởi tạo S3 Client
s3_client = boto3.client('s3')
BUCKET_NAME = 'store-aws-blogs-and-translated-version'

# --- CẤU HÌNH AWS & GOOGLE ---
try:
    GOOGLE_API_CREDENTIALS = json.loads(os.environ.get('GOOGLE_CREDENTIALS', '{}'))
except json.JSONDecodeError:
    GOOGLE_API_CREDENTIALS = {} 
    
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

def get_aws_blog_content(url):
    """Trích xuất Metadata và chuyển HTML nội dung blog AWS sang Markdown chuẩn."""
    if not url or not url.startswith('http'):
        return {"error": f"URL blog AWS không hợp lệ: {url}"}
        
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status() 
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 1. CÀO METADATA
        title_tag = soup.find('meta', property='og:title')
        title = title_tag['content'].split(' | ')[0] if title_tag else "No Title"
        
        author_tag = soup.find('meta', attrs={'name': 'author'})
        author = author_tag['content'] if author_tag else "Unknown Author"
        
        date_tag = soup.find('meta', property='article:published_time')
        date = date_tag['content'][:10] if date_tag else "Unknown Date"
        
        # 2. CÀO NỘI DUNG VÀ CONVERT SANG MARKDOWN
        article_body = soup.select_one('article .blog-post-content')
        
        if article_body:
            # Dùng markdownify biến toàn bộ khối HTML thành Markdown, giữ nguyên link, code, bold...
            content_md = md(str(article_body), heading_style="ATX")
        else:
            content_md = "Không tìm thấy nội dung bài viết."
            
        return {
            "title": title,
            "author": author,
            "date": date,
            "content": content_md.strip()
        }
    except requests.RequestException as e:
        return {"error": f"Lỗi khi truy cập URL blog AWS: {e}"}

def get_google_doc_content(url):
    """Trích xuất nội dung và chuyển đổi định dạng Google Docs sang Markdown."""
    if not url or 'docs.google.com/document/d/' not in url:
        return f"Lỗi: URL Google Docs không hợp lệ. URL nhận được: '{url}'"
    
    try:
        if not GOOGLE_API_CREDENTIALS:
            return "Lỗi: Biến môi trường GOOGLE_CREDENTIALS chưa được cấu hình hoặc sai định dạng."
        
        creds = service_account.Credentials.from_service_account_info(GOOGLE_API_CREDENTIALS, scopes=SCOPES)
        service = build('docs', 'v1', credentials=creds)
        
        document_id = url.split('/d/')[1].split('/')[0]
        document = service.documents().get(documentId=document_id).execute()
        
        content = document.get('body', {}).get('content')
        doc_text = ''
        
        if content:
            for value in content:
                if 'paragraph' in value:
                    para = value['paragraph']
                    
                    # 1. Bắt các thẻ Heading (H1, H2, H3...)
                    style_type = para.get('paragraphStyle', {}).get('namedStyleType', '')
                    prefix = ""
                    if style_type == 'HEADING_1': prefix = "# "
                    elif style_type == 'HEADING_2': prefix = "## "
                    elif style_type == 'HEADING_3': prefix = "### "
                    elif style_type == 'HEADING_4': prefix = "#### "
                    
                    para_text = prefix
                    
                    # 2. Bắt Format cho từng đoạn text (Bold, Italic, Link)
                    for elem in para.get('elements', []):
                        if 'textRun' in elem:
                            text_run = elem['textRun']
                            raw_content = text_run.get('content', '')
                            
                            # Bỏ qua nếu chỉ là khoảng trắng/xuống dòng
                            if not raw_content.strip():
                                para_text += raw_content
                                continue
                                
                            style = text_run.get('textStyle', {})
                            
                            # Tách khoảng trắng ở đầu/cuối để bọc Markdown không bị lỗi cú pháp
                            stripped = raw_content.strip()
                            leading = raw_content[:len(raw_content) - len(raw_content.lstrip())]
                            trailing = raw_content[len(raw_content.rstrip()):]
                            
                            formatted = stripped
                            
                            # Xử lý Link
                            if 'link' in style and 'url' in style['link']:
                                formatted = f"[{formatted}]({style['link']['url']})"
                            # Xử lý In đậm
                            if style.get('bold'):
                                formatted = f"**{formatted}**"
                            # Xử lý In nghiêng
                            if style.get('italic'):
                                formatted = f"*{formatted}*"
                                
                            # Ráp lại hoàn chỉnh
                            para_text += f"{leading}{formatted}{trailing}"
                            
                    doc_text += para_text
                    
        return doc_text.strip()
    except Exception as e:
        return f"Lỗi khi xử lý Google Docs API: {e}"

def lambda_handler(event, context):
    extracted_contents = [] 
    records_count = len(event.get('Records', []))
    print(f"Bắt đầu xử lý {records_count} message(s) từ SQS.")

    for record in event.get('Records', []):
        payload_str = record.get('body', '{}')
        try:
            payload = json.loads(payload_str)
            aws_blog_url = payload.get('aws_blog_url')
            google_doc_url = payload.get('google_doc_url')

            if not aws_blog_url or not google_doc_url:
                continue

            print(f"Bắt đầu trích xuất AWS Blog: {aws_blog_url}")
            aws_data = get_aws_blog_content(aws_blog_url)
            
            if "error" in aws_data:
                print(f"Lỗi trích xuất AWS Blog: {aws_data['error']}")
                continue
                
            print(f"Bắt đầu trích xuất Google Doc: {google_doc_url}")
            gdoc_content = get_google_doc_content(google_doc_url)
            
            if gdoc_content.startswith("Lỗi:"):
                print(f"Lỗi trích xuất Google Doc: {gdoc_content}")
                continue

            # === GẮN FRONTMATTER ===
            metadata_header = json.dumps({
                "englishTitle": aws_data["title"],
                "author": aws_data["author"],
                "publishDate": aws_data["date"]
            }, ensure_ascii=False)
            
            frontmatter_block = f"{metadata_header}\n---METADATA_END---\n"
            final_original_content = frontmatter_block + aws_data["content"]
            final_translated_content = frontmatter_block + gdoc_content

            # === LƯU LÊN S3 ===
            article_id = aws_blog_url.strip('/').split('/')[-1]

            print(f"Đang lưu file lên S3 với ID: {article_id}")
            
            s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=f"original/{article_id}.md",
                Body=final_original_content.encode('utf-8')
            )
            
            s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=f"translated/{article_id}.md",
                Body=final_translated_content.encode('utf-8')
            )

            extracted_contents.append({"article_id": article_id, "status": "Saved to S3"})
            print(f"Hoàn tất lưu trữ bài viết: {article_id}")

        except Exception as e:
            print(f"Lỗi nghiêm trọng: {e}")
            continue

    final_message = f'Hoàn tất xử lý. Đã lưu thành công {len(extracted_contents)} / {records_count} bài báo lên S3.'
    
    return {
        'statusCode': 200,
        'headers': { 'Content-Type': 'application/json' },
        'body': json.dumps({
            'message': final_message,
            'details': extracted_contents 
        }, ensure_ascii=False, indent=2)
    }
import json
import os
import requests
from bs4 import BeautifulSoup
from google.oauth2 import service_account
from googleapiclient.discovery import build

# --- CẤU HÌNH AWS & GOOGLE ---
try:
    GOOGLE_API_CREDENTIALS = json.loads(os.environ.get('GOOGLE_CREDENTIALS', '{}'))
except json.JSONDecodeError:
    GOOGLE_API_CREDENTIALS = {} 
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

def get_aws_blog_content(url):
    """Trích xuất nội dung văn bản từ một URL blog của AWS."""
    if not url or not url.startswith('http'):
        return f"Lỗi: URL blog AWS không hợp lệ: {url}"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status() 
        soup = BeautifulSoup(response.content, 'html.parser')
        article_body = soup.select_one('article .blog-post-content')
        return article_body.get_text(separator='\n', strip=True) if article_body else "Không tìm thấy nội dung bài viết."
    except requests.RequestException as e:
        return f"Lỗi khi truy cập URL blog AWS: {e}"

def get_google_doc_content(url):
    """Trích xuất nội dung văn bản từ một URL Google Docs."""
    if not url or 'docs.google.com/document/d/' not in url:
        return f"Lỗi: URL Google Docs không hợp lệ. URL nhận được: '{url}'"
    
    try:
        if not GOOGLE_API_CREDENTIALS:
            return "Lỗi: Biến môi trường GOOGLE_CREDENTIALS chưa được cấu hình."
        
        creds = service_account.Credentials.from_service_account_info(
            GOOGLE_API_CREDENTIALS, scopes=SCOPES)
        service = build('docs', 'v1', credentials=creds)
        
        document_id = url.split('/d/')[1].split('/')[0]
        document = service.documents().get(documentId=document_id).execute()
        
        content = document.get('body', {}).get('content')
        doc_text = ''
        if content:
            for value in content:
                if 'paragraph' in value:
                    elements = value.get('paragraph', {}).get('elements', [])
                    for elem in elements:
                        if 'textRun' in elem:
                            doc_text += elem.get('textRun', {}).get('content', '')
        return doc_text.strip()
    except Exception as e:
        return f"Lỗi khi xử lý Google Docs API: {e}"

def lambda_handler(event, context):
    """Hàm xử lý test trực tiếp trên Console."""
    print(f"Bắt đầu xử lý với Test Event: {json.dumps(event)}")

    # Lấy trực tiếp URL từ event
    aws_blog_url = event.get('aws_blog_url')
    google_doc_url = event.get('google_doc_url')

    if not aws_blog_url or not google_doc_url:
        error_msg = "Lỗi: Thiếu aws_blog_url hoặc google_doc_url trong Test Event."
        print(error_msg)
        return {
            'statusCode': 400,
            'body': json.dumps({'error': error_msg}, ensure_ascii=False)
        }

    # === TRÍCH XUẤT ===
    print(f"Đang cào AWS Blog: {aws_blog_url}")
    aws_content = get_aws_blog_content(aws_blog_url)
    print(f"-> Hoàn tất AWS Blog. Ký tự: {len(aws_content)}")

    print(f"Đang cào Google Doc: {google_doc_url}")
    gdoc_content = get_google_doc_content(google_doc_url)
    print(f"-> Hoàn tất Google Doc. Ký tự: {len(gdoc_content)}")

    # Gom data
    result_payload = {
        "original_article_content": aws_content,
        "translated_article_content": gdoc_content,
        "source_info": {
            "aws_blog_url": aws_blog_url,
            "google_doc_url": google_doc_url
        }
    }

    print("Hoàn tất Test run.")
    return {
        'statusCode': 200,
        'headers': { 'Content-Type': 'application/json' },
        'body': json.dumps({
            'message': 'Trích xuất thành công',
            'extracted_data': result_payload 
        }, ensure_ascii=False, indent=2)
    }
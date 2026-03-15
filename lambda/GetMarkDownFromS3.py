import json
import boto3
import os

s3 = boto3.client('s3')
BUCKET_NAME = "store-aws-blogs-and-translated-version"

def format_english_text(text):
    """
    Đọc cục JSON ở đầu file tiếng Anh, trích xuất thông tin 
    và đắp thành Header đẹp mắt cho giống format của bài tiếng Việt.
    """
    delimiter = "---METADATA_END---"
    if delimiter in text:
        parts = text.split(delimiter, 1)
        meta_raw = parts[0].strip()
        body = parts[1].lstrip()
        
        try:
            # Parse cái cục JSON ở đầu file
            meta = json.loads(meta_raw)
            title = meta.get("englishTitle", "No Title")
            author = meta.get("author", "Unknown Author")
            date = meta.get("publishDate", "")
            
            # Lắp ráp lại thành format xuống dòng giống bản dịch
            header = f"{title}\nAuthor: {author}\nPublish Date: {date}\n\n"
            
            return header + body
        except Exception as e:
            print("Lỗi khi parse Metadata JSON:", e)
            return body
            
    return text

def remove_metadata(text):
    """Tìm và gọt bỏ phần JSON Metadata ở đầu file, y hệt bên Chunking"""
    delimiter = "---METADATA_END---"
    if delimiter in text:
        return text.split(delimiter, 1)[1].lstrip()
    return text

def lambda_handler(event, context):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS"
    }
    
    try:
        query_params = event.get('queryStringParameters', {})
        article_id = query_params.get('article_id')
        
        if not article_id:
            return {"statusCode": 400, "headers": headers, "body": json.dumps({"msg": "Missing article_id"})}

        # Tải bản dịch (translated) từ S3
        trans_obj = s3.get_object(Bucket=BUCKET_NAME, Key=f"translated/{article_id}.md")
        translated_text = trans_obj['Body'].read().decode('utf-8')
        
        # Tải bản gốc (original) từ S3
        orig_obj = s3.get_object(Bucket=BUCKET_NAME, Key=f"original/{article_id}.md")
        original_text = orig_obj['Body'].read().decode('utf-8')

        # ---> BƯỚC ĐỒNG BỘ FORMAT Ở ĐÂY <---
        # Bản Anh: Tái chế Metadata thành Text Header
        original_text = format_english_text(original_text)
        
        # Bản Việt: Chặt bỏ Metadata (vì nội dung đã có sẵn title do người dịch gõ)
        translated_text = remove_metadata(translated_text)

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({
                "originalText": original_text,
                "translatedText": translated_text
            })
        }
    except Exception as e:
        return {"statusCode": 500, "headers": headers, "body": json.dumps({"error": str(e)})}
import json
import boto3
import os
import base64
import io
import pandas as pd 
from botocore.exceptions import ClientError

# --- CẤU HÌNH ---
# Lấy URL từ biến môi trường (Environment Variables) để bảo mật và linh hoạt
SQS_QUEUE_URL = os.environ.get('SQS_QUEUE_URL')
sqs_client = boto3.client('sqs')

COLUMN_AWS_URL = 'aws_blog_url'
COLUMN_GDOC_URL = 'google_doc_url'

def send_to_sqs(aws_url, gdoc_url):
    """Gửi message vào SQS"""
    message_body = {
        'aws_blog_url': aws_url,
        'google_doc_url': gdoc_url
    }
    try:
        response = sqs_client.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(message_body)
        )
        return response['MessageId']
    except ClientError as e:
        print(f"Error sending to SQS: {e}")
        return None

def lambda_handler(event, context):
    print("Received event")
    
    # 1. Kiểm tra biến môi trường
    if not SQS_QUEUE_URL:
        return http_response(500, "Server Error: SQS_QUEUE_URL is not configured.")

    # 2. Lấy dữ liệu file từ Body của API Gateway
    try:
        body = event.get('body', '')
        is_base64 = event.get('isBase64Encoded', False)
        
        if not body:
            return http_response(400, "No file content found in request body.")

        # Decode dữ liệu nếu là Base64 (Thường API Gateway sẽ encode binary file)
        if is_base64:
            file_content = base64.b64decode(body)
        else:
            file_content = body.encode('utf-8')

        # 3. Đọc dữ liệu vào Pandas DataFrame
        # Dùng io.BytesIO để giả lập file trên RAM
        try:
            # Thử đọc như Excel trước
            df = pd.read_excel(io.BytesIO(file_content))
        except:
            try:
                # Nếu lỗi thì thử đọc như CSV
                df = pd.read_csv(io.BytesIO(file_content))
            except Exception as e:
                return http_response(400, f"Invalid file format. Please upload .xlsx or .csv. Error: {str(e)}")

        # 4. Validate cột
        if COLUMN_AWS_URL not in df.columns or COLUMN_GDOC_URL not in df.columns:
            return http_response(400, f"Missing columns. File must contain: '{COLUMN_AWS_URL}' and '{COLUMN_GDOC_URL}'")

        # 5. Lặp và gửi SQS
        success_count = 0
        total_rows = len(df)
        
        for index, row in df.iterrows():
            aws_url = row[COLUMN_AWS_URL]
            gdoc_url = row[COLUMN_GDOC_URL]

            if pd.isna(aws_url) or pd.isna(gdoc_url):
                continue
                
            msg_id = send_to_sqs(str(aws_url), str(gdoc_url))
            if msg_id:
                success_count += 1

        # 6. Trả về kết quả
        return http_response(200, {
            "message": "File processed successfully",
            "total_rows": total_rows,
            "success_sent": success_count
        })

    except Exception as e:
        print(f"Critical Error: {str(e)}")
        return http_response(500, f"Internal Server Error: {str(e)}")

def http_response(code, body):
    """Hàm helper để trả về format chuẩn và xử lý CORS cho API Gateway"""
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS, POST",
            "Access-Control-Allow-Headers": "Content-Type, Authorization" 
        },
        "body": json.dumps(body) if isinstance(body, dict) else json.dumps({"message": body})
    }
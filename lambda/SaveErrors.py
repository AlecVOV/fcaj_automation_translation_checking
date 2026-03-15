import json
import boto3
import os
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME')

def lambda_handler(event, context):
    print("INPUT FROM JANITOR:", json.dumps(event))
    
    table = dynamodb.Table(TABLE_NAME)
    
    # 1. Lấy dữ liệu đã được lọc sạch
    article_id = event.get('article_id')
    clean_errors = event.get('clean_errors', [])
    
    if not article_id:
        return {"status": "error", "msg": "Missing article_id"}

    article_pk = f"ART#{article_id}"
    
    try:
        # 2. Lưu hàng loạt lỗi vào DynamoDB (Dùng Batch Writer để tối ưu)
        with table.batch_writer() as batch:
            for err in clean_errors:
                batch.put_item(Item={
                    "PK": article_pk,
                    "SK": f"ERR#{uuid.uuid4().hex[:8]}", # Tạo ID lỗi ngẫu nhiên
                    "RecordType": "ErrorDetail",
                    
                    # Dữ liệu từ AI đã được Janitor chuẩn hóa
                    "ErrorType": err.get('ErrorType', 'General'),
                    "Severity": err.get('Severity', 'Minor'),
                    "OriginalText": err.get('OriginalText', ''),
                    "CurrentTranslation": err.get('CurrentTranslation', ''),
                    "SuggestedFix": err.get('SuggestedFix', ''),
                    "Explanation": err.get('Explanation', ''),
                    
                    "CreatedAt": datetime.now().isoformat()
                })

        # 3. Cập nhật Metadata tổng của bài viết
        # Vì lưu một lần duy nhất nên ErrorCount chính là độ dài mảng clean_errors
        table.update_item(
            Key={'PK': article_pk, 'SK': 'METADATA'},
            UpdateExpression="SET ErrorCount = :count, #s = :status, LastUpdated = :now, RecordType = :rtype",
            ExpressionAttributeNames={'#s': 'Status'}, # Tránh lỗi Reserved Keyword
            ExpressionAttributeValues={
                ':count': len(clean_errors),
                ':status': 'Ready', # Chuyển trạng thái sang Ready để Dashboard hiện lên
                ':now': datetime.now().isoformat(),
                ':rtype': 'Metadata'
            }
        )
        
        return {
            "status": "success", 
            "article_id": article_id,
            "total_saved": len(clean_errors)
        }

    except Exception as e:
        print(f"Error saving to DB: {str(e)}")
        return {"status": "error", "msg": str(e)}
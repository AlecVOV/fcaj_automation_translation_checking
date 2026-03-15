import json
import boto3
import os
from boto3.dynamodb.conditions import Key
from decimal import Decimal

# Khởi tạo DynamoDB Resource
dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME')
table = dynamodb.Table(TABLE_NAME)

# Class hỗ trợ convert Decimal sang Int/Float (vì JSON mặc định không hiểu Decimal của DynamoDB)
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    # 1. Lấy headers để xử lý CORS (quan trọng cho Web App gọi API)
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    try:
        # 2. Lấy article_id từ Query String Parameters (VD: /errors?article_id=abc)
        query_params = event.get('queryStringParameters')
        if not query_params or 'article_id' not in query_params:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"message": "Missing article_id parameter"})
            }
        
        article_id = query_params['article_id']
        
        # 3. Tạo Partition Key (PK) để truy vấn
        # LƯU Ý: Phải khớp với cách bạn lưu trong hàm SaveValidation.
        # Giả sử bạn lưu là "ARTICLE#<id>", nếu lưu chỉ là "<id>" thì sửa dòng dưới.
        pk_value = f"ART#{article_id}" 

        print(f"Querying DynamoDB with PK: {pk_value}")

        # 4. Thực hiện Query (Hiệu quả hơn Scan)
        response = table.query(
            KeyConditionExpression=Key('PK').eq(pk_value) & Key('SK').begins_with('ERR#')
        )
        
        items = response.get('Items', [])
        
        print(f"Found {len(items)} errors.")

        # 5. Trả về kết quả
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({
                "article_id": article_id,
                "total_errors": len(items),
                "errors": items
            }, cls=DecimalEncoder) # Dùng class DecimalEncoder để tránh lỗi
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"message": "Internal Server Error", "error": str(e)})
        }
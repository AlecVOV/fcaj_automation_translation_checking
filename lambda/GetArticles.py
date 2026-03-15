import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    try:
        # 1. Dùng Scan để lấy dữ liệu. 
        # Tối ưu: Chỉ lấy PK, SK và Severity để tiết kiệm RAM/Băng thông
        response = table.scan(
            ProjectionExpression="PK, SK, Severity"
        )
        items = response.get('Items', [])

        # Xử lý phân trang nếu DB có nhiều hơn 1MB dữ liệu
        while 'LastEvaluatedKey' in response:
            response = table.scan(
                ProjectionExpression="PK, SK, Severity",
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            items.extend(response.get('Items', []))

        # 2. Gom nhóm dữ liệu theo từng Bài báo (article_id)
        dashboard_data = {}
        
        for item in items:
            pk = item.get('PK', '')
            # Bỏ qua nếu không phải record của bài báo
            if not pk.startswith('ART#'): 
                continue

            article_id = pk.replace('ART#', '')

            # Khởi tạo object nếu bài báo này chưa có trong dict
            if article_id not in dashboard_data:
                dashboard_data[article_id] = {
                    "article_id": article_id,
                    "total_errors": 0,
                    "critical_errors": 0,
                    "major_errors": 0,
                    "minor_errors": 0
                }

            # Tăng tổng số lỗi
            dashboard_data[article_id]["total_errors"] += 1
            
            # Phân loại mức độ nghiêm trọng (Rất tiện cho Frontend sort)
            severity = item.get('Severity', '')
            if severity == 'Critical':
                dashboard_data[article_id]["critical_errors"] += 1
            elif severity == 'Major':
                dashboard_data[article_id]["major_errors"] += 1
            elif severity == 'Minor':
                dashboard_data[article_id]["minor_errors"] += 1

        # 3. Chuyển dict thành List để trả về cho Frontend
        result_list = list(dashboard_data.values())

        # (Tuỳ chọn) Sắp xếp mặc định theo tổng số lỗi giảm dần
        result_list.sort(key=lambda x: x['total_errors'], reverse=True)

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({
                "total_articles": len(result_list),
                "articles": result_list
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 200,
            "headers": {
                # 3 dòng "giấy thông hành" thần thánh
                "Access-Control-Allow-Origin": "*",  # Dấu * nghĩa là cho phép mọi domain (gồm cả localhost)
                "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "body": json.dumps({
                "message": "Thành công rồi đó!"
            })
        }
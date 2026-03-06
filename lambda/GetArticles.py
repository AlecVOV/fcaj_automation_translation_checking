import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME')
table = dynamodb.Table(TABLE_NAME)

HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
}

def lambda_handler(event, context):
    # Handle preflight OPTIONS request
    if event.get('httpMethod') == 'OPTIONS':
        return {"statusCode": 200, "headers": HEADERS, "body": json.dumps({})}

    try:
        response = table.scan(ProjectionExpression="PK, SK, Severity")
        items = response.get('Items', [])

        while 'LastEvaluatedKey' in response:
            response = table.scan(
                ProjectionExpression="PK, SK, Severity",
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            items.extend(response.get('Items', []))

        dashboard_data = {}
        for item in items:
            pk = item.get('PK', '')
            if not pk.startswith('ART#'):
                continue
            article_id = pk.replace('ART#', '')
            if article_id not in dashboard_data:
                dashboard_data[article_id] = {
                    "article_id": article_id,
                    "total_errors": 0,
                    "critical_errors": 0,
                    "major_errors": 0,
                    "minor_errors": 0,
                }
            dashboard_data[article_id]["total_errors"] += 1
            severity = item.get('Severity', '')
            if severity == 'Critical':
                dashboard_data[article_id]["critical_errors"] += 1
            elif severity == 'Major':
                dashboard_data[article_id]["major_errors"] += 1
            elif severity == 'Minor':
                dashboard_data[article_id]["minor_errors"] += 1

        result_list = sorted(dashboard_data.values(), key=lambda x: x['total_errors'], reverse=True)

        return {
            "statusCode": 200,
            "headers": HEADERS,
            "body": json.dumps({"total_articles": len(result_list), "articles": result_list}),
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": HEADERS,
            "body": json.dumps({"message": str(e)}),
        }
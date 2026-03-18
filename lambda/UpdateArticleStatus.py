import json
import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME')

VALID_STATUSES = ['Ready', 'In Review', 'Approved', 'Published']

def lambda_handler(event, context):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization"
    }

    try:
        # 1. Parse request body
        body = json.loads(event.get('body', '{}'))
        article_id = body.get('article_id')
        new_status = body.get('new_status')

        # 2. Validate inputs
        if not article_id:
            return {"statusCode": 400, "headers": headers, "body": json.dumps({"message": "Missing article_id"})}

        if new_status not in VALID_STATUSES:
            return {"statusCode": 400, "headers": headers, "body": json.dumps({
                "message": f"Invalid status. Must be one of: {VALID_STATUSES}"
            })}

        # 3. Get reviewer email from Cognito JWT claims (if available)
        updated_by = "unknown"
        request_context = event.get('requestContext', {})
        authorizer = request_context.get('authorizer', {})
        claims = authorizer.get('claims', {})
        if claims.get('email'):
            updated_by = claims['email']

        # 4. Update METADATA item in DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        table.update_item(
            Key={'PK': f"ART#{article_id}", 'SK': 'METADATA'},
            UpdateExpression="SET #s = :status, LastUpdated = :now, UpdatedBy = :user",
            ExpressionAttributeNames={'#s': 'Status'},
            ExpressionAttributeValues={
                ':status': new_status,
                ':now': datetime.now().isoformat(),
                ':user': updated_by
            }
        )

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({
                "message": "Status updated successfully",
                "article_id": article_id,
                "new_status": new_status
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"message": f"Internal Server Error: {str(e)}"})
        }
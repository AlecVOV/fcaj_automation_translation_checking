import json
import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME')

def lambda_handler(event, context):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization"
    }

    try:
        body = json.loads(event.get('body', '{}'))
        article_id = body.get('article_id')
        accepted_error_ids = body.get('accepted_error_ids', [])

        if not article_id:
            return {"statusCode": 400, "headers": headers, "body": json.dumps({"message": "Missing article_id"})}

        if not isinstance(accepted_error_ids, list):
            return {"statusCode": 400, "headers": headers, "body": json.dumps({"message": "accepted_error_ids must be a list"})}

        # Get reviewer email from Cognito JWT claims
        reviewed_by = "unknown"
        claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
        if claims.get('email'):
            reviewed_by = claims['email']

        table = dynamodb.Table(TABLE_NAME)
        table.update_item(
            Key={'PK': f"ART#{article_id}", 'SK': 'METADATA'},
            UpdateExpression="SET AcceptedErrorIds = :ids, ReviewedBy = :reviewer, LastUpdated = :now",
            ExpressionAttributeValues={
                ':ids': accepted_error_ids,
                ':reviewer': reviewed_by,
                ':now': datetime.now().isoformat()
            }
        )

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({
                "message": "Review progress saved",
                "article_id": article_id,
                "accepted_count": len(accepted_error_ids)
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"message": f"Internal Server Error: {str(e)}"})
        }
import json
import boto3
import os
import time
from datetime import datetime, timezone

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
        note_text = body.get('note_text', '').strip()

        if not article_id:
            return {"statusCode": 400, "headers": headers, "body": json.dumps({"message": "Missing article_id"})}

        if not note_text:
            return {"statusCode": 400, "headers": headers, "body": json.dumps({"message": "Missing note_text"})}

        # Get author email from Cognito JWT claims
        written_by = "Admin FCJ"
        claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
        if claims.get('email'):
            written_by = claims['email']

        # Use millisecond timestamp as SK for chronological ordering
        timestamp_ms = str(int(time.time() * 1000))
        created_at = datetime.now(timezone.utc).isoformat()

        table = dynamodb.Table(TABLE_NAME)
        table.put_item(
            Item={
                'PK': f"ART#{article_id}",
                'SK': f"NOTE#{timestamp_ms}",
                'NoteText': note_text,
                'WrittenBy': written_by,
                'CreatedAt': created_at
            }
        )

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({
                "message": "Note saved",
                "article_id": article_id,
                "note_id": timestamp_ms,
                "written_by": written_by,
                "created_at": created_at
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"message": f"Internal Server Error: {str(e)}"})
        }
import json
import boto3
import os
from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME')
table = dynamodb.Table(TABLE_NAME)

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization"
    }

    try:
        query_params = event.get('queryStringParameters') or {}
        article_id = query_params.get('article_id')

        if not article_id:
            return {"statusCode": 400, "headers": headers, "body": json.dumps({"message": "Missing article_id parameter"})}

        pk_value = f"ART#{article_id}"

        response = table.query(
            KeyConditionExpression=Key('PK').eq(pk_value) & Key('SK').begins_with('NOTE#')
        )
        items = response.get('Items', [])

        # Already sorted chronologically by SK (NOTE#timestamp_ms)
        notes = []
        for item in items:
            notes.append({
                "note_id": item['SK'].replace('NOTE#', ''),
                "note_text": item.get('NoteText', ''),
                "written_by": item.get('WrittenBy', 'Admin FCJ'),
                "created_at": item.get('CreatedAt', '')
            })

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({
                "article_id": article_id,
                "total_notes": len(notes),
                "notes": notes
            }, cls=DecimalEncoder)
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"message": f"Internal Server Error: {str(e)}"})
        }
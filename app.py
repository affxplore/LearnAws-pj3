import json
import boto3
import os
import uuid
from boto3.dynamodb.conditions import Key

# Ambil nama tabel dari environment variable
TABLE_NAME = os.environ.get('TABLE_NAME')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    print("Event received:", json.dumps(event))
    
    path = event.get('path')
    http_method = event.get('httpMethod')
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*', # Penting untuk CORS
        'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,DELETE',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
    }

    try:
        if http_method == 'GET' and path == '/tasks':
            # Ambil semua data dari DynamoDB (kurang efisien untuk data besar, tapi ok untuk latihan)
            response = table.scan()
            tasks = response.get('Items', [])
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(tasks)
            }
            
        elif http_method == 'POST' and path == '/tasks':
            body = json.loads(event.get('body', '{}'))
            task_id = str(uuid.uuid4())
            task_name = body.get('task_name', 'Unnamed Task')
            
            item = {
                'taskId': task_id,
                'taskName': task_name,
                'status': 'pending'
            }
            table.put_item(Item=item)
            return {
                'statusCode': 201,
                'headers': headers,
                'body': json.dumps({'message': 'Task created', 'taskId': task_id})
            }
            
        elif http_method == 'OPTIONS':
            # Respon untuk preflight request CORS
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({})
            }
        else:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'message': f'Unsupported method {http_method} or path {path}'})
            }
            
    except Exception as e:
        print("Error:", e)
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': str(e)})
        }
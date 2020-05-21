import os
import json
import uuid
import boto3
import decimal

# get the service resource
dynamodb = boto3.resource('dynamodb')
# get the users table
USERS_TABLE = os.environ['USERS_TABLE']

def lambda_handler(event, context):
    
    users_table = dynamodb.Table(USERS_TABLE)
    user_id = event['pathParameters']['user_id']

    try:
        response = users_table.get_item(Key={'id': user_id})
        res = str(json.dumps(response, default=str))
        item = response['Item']
        print(f'get_item result: {res}')
        statusCode = 200
        body = json.dumps({
            'user_id': item['id'],
            'credit': item['credit']
        }, default=str)
    except Exception as e:
        print(f'get_item error: {e}')
        statusCode = 400
        body = json.dumps({})

    return {
        "statusCode": statusCode,
        "body": body
    }
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
    user_id = str(uuid.uuid4())

    try:
        response = users_table.put_item(Item = {'id': user_id, 'credit': decimal.Decimal('0.0')})
        res = json.dumps(response, default=str)
        statusCode = 200
        body = json.dumps({
            'user_id': user_id
        })
        print(f'put_item result: {res}')
    except Exception as e:
        statusCode = 400
        body = json.dumps({})
        print(f'put_item error: {e}')

    return {
        "statusCode": statusCode,
        "body": body
    }
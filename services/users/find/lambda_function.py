import json
import os

import boto3

# get the service resource
dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table(os.environ['USERS_TABLE'])


def lambda_handler(event, context):
    user_id = event['pathParameters']['user_id']

    print(f'users_find: {user_id}')

    try:
        response = users_table.get_item(Key={'id': user_id}, ConsistentRead=True)
        res = json.dumps(response, default=str)
        item = response['Item']
        print(f'get_item result: {res}')
        status_code = 200
        body = json.dumps({
            'user_id': item['id'],
            'credit': item['credit']
        }, default=str)
    except Exception as e:
        print(f'get_item error: {e}')
        status_code = 400
        body = json.dumps({})

    return {
        "statusCode": status_code,
        "body": body
    }

import json
import os

import boto3

# get the service resource
dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table(os.environ['USERS_TABLE'])


def lambda_handler(event, context):
    user_id = event['pathParameters']['user_id']

    try:
        response = users_table.delete_item(Key={'id': user_id})
        res = json.dumps(response, default=str)
        print(f'user successfully removed: {res}')
        status_code = 200
    except Exception as e:
        print(f'delete_item error: {e}')
        status_code = 400

    return {
        "statusCode": status_code
    }
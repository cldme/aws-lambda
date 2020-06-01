import os
import json
import uuid
import boto3
import decimal

# get the service resource
dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table(os.environ['USERS_TABLE'])


def lambda_handler(event, context):
    user_id = event['pathParameters']['user_id']

    try:
        response = users_table.delete_item(Key={'id': user_id})
        res = json.dumps(response, default=str)
        print(f'user successfully removed: {res}')
        statusCode = 200
    except Exception as e:
        print(f'delete_item error: {e}')
        statusCode = 400

    return {
        "statusCode": statusCode
    }
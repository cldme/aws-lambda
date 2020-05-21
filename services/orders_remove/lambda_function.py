import os
import json
import uuid
import boto3
import decimal

# get the service resource
dynamodb = boto3.resource('dynamodb')
# get the users table
ORDERS_TABLE = os.environ['ORDERS_TABLE']

def lambda_handler(event, context):

    orders_table = dynamodb.Table(ORDERS_TABLE)
    order_id = event['pathParameters']['order_id']

    try:
        response = orders_table.delete_item(Key={'id': order_id})
        res = json.dumps(response, default=str)
        print(f'order successfully removed: {res}')
        statusCode = 200
    except Exception as e:
        print(f'delete_item error: {e}')
        statusCode = 400

    return {
        "statusCode": statusCode
    }
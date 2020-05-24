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
        response = orders_table.get_item(Key={'id': order_id})
        res = json.dumps(response, default=str)
        item = response['Item']
        print(f'get_item result: {res}')
        statusCode = 200
        body = json.dumps({
            'order_id': item['id'],
            'paid': item['paid'],
            'items': item['items'],
            'user_id': item['user_id'],
            'total_cost': item['total_cost']
        }, default=str)
    except Exception as e:
        print(f'get_item error: {e}')
        statusCode = 400
        body = json.dumps({})

    return {
        "statusCode": statusCode,
        "body": body
    }
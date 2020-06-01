import os
import json
import uuid
import boto3
import decimal

# get the service resource
dynamodb = boto3.resource('dynamodb')
stock_table = dynamodb.Table(os.environ['STOCK_TABLE'])


def lambda_handler(event, context):
    item_id = event['pathParameters']['item_id']

    try:
        response = stock_table.get_item(Key={'id': item_id})
        res = json.dumps(response, default=str)
        item = response['Item']
        print(f'get_item result: {res}')
        statusCode = 200
        body = json.dumps({
            'item_id': item['id'],
            'stock': item['stock'],
            'price': item['price']
        }, default=str)
    except Exception as e:
        print(f'get_item error: {e}')
        statusCode = 400
        body = json.dumps({})

    return {
        "statusCode": statusCode,
        "body": body
    }
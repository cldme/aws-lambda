import json
import os

import boto3

dynamodb = boto3.resource('dynamodb')
ORDERS_TABLE = os.environ['ORDERS_TABLE']


def lambda_handler(event, context):
    orders_table = dynamodb.Table(ORDERS_TABLE)
    order_id = event['pathParameters']['order_id']

    try:
        response = orders_table.get_item(Key={'id': order_id})
        item = response['Item']
        status_code = 200
        body = json.dumps({
            'paid': item['paid'],
        })
    except Exception as e:
        print(f'status error: {e}')
        status_code = 400
        body = json.dumps({})

    return {
        "statusCode": status_code,
        "body": body
    }

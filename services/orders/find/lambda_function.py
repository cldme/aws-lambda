import os
import json
import uuid
import boto3
import decimal

# get the service resource
dynamodb = boto3.resource('dynamodb')
orders_table = dynamodb.Table(os.environ['ORDERS_TABLE'])


def lambda_handler(event, context):
    order_id = event['pathParameters']['order_id']

    try:
        response = orders_table.get_item(Key={'id': order_id})
        res = json.dumps(response, default=str)
        item = response['Item']
        print(f'get_item result: {res}')
        status_code = 200
        body = json.dumps({
            'order_id': item['id'],
            'paid': item['paid'],
            'items': list([item_id for k, v in item['items'].items() for item_id in [k] * int(v)]),
            'user_id': item['user_id'],
            'total_cost': item['total_cost']
        }, default=str)
    except Exception as e:
        print(f'get_item error: {e}')
        status_code = 400
        body = json.dumps({})

    return {
        "statusCode": status_code,
        "body": body
    }

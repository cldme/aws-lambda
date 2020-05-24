import json
import os

import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
ORDERS_TABLE = os.environ['ORDERS_TABLE']


def lambda_handler(event, context):
    orders_table = dynamodb.Table(ORDERS_TABLE)
    order_id = event['pathParameters']['order_id']

    try:
        response = orders_table.get_item(Key={'id': order_id})
        item = response['Item']
        statusCode = 200
        body = json.dumps({
            'paid': item['paid'],
        })
    except ClientError as e:
        print(f'status error: {e}')
        statusCode = 400
        body = json.dumps({})

    return {
        "statusCode": statusCode,
        "body": body
    }

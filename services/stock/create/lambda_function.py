import decimal
import json
import os
import uuid

import boto3

# get the service resource
dynamodb = boto3.resource('dynamodb')
stock_table = dynamodb.Table(os.environ['STOCK_TABLE'])


def lambda_handler(event, context):
    price = event['pathParameters']['price']
    item_id = str(uuid.uuid4())

    try:
        response = stock_table.put_item(
            Item={
                'id': item_id,
                'stock': 0,
                'price': decimal.Decimal(price)
            }
        )
        res = json.dumps(response, default=str)
        status_code = 200
        body = json.dumps({
            'item_id': item_id
        })
        print(f'put_item result: {res}')
    except Exception as e:
        status_code = 400
        body = json.dumps({})
        print(f'put_item error: {e}')

    return {
        "statusCode": status_code,
        "body": body
    }

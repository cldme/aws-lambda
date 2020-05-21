import os
import json
import uuid
import boto3
import decimal

# get the service resource
dynamodb = boto3.resource('dynamodb')
# get the users table
STOCK_TABLE = os.environ['STOCK_TABLE']

def lambda_handler(event, context):
    
    stock_table = dynamodb.Table(STOCK_TABLE)
    price = event['pathParameters']['price']
    item_id = str(uuid.uuid4())

    try:
        response = stock_table.put_item(
            Item = {
                'id': item_id, 
                'stock': decimal.Decimal('0.0'),
                'price': decimal.Decimal(price)
            }
        )
        res = str(json.dumps(response, default=str))
        statusCode = 200
        body = json.dumps({
            'item_id': item_id
        })
        print(f'put_item result: {res}')
    except Exception as e:
        statusCode = 400
        body = json.dumps({})
        print(f'put_item error: {e}')

    return {
        "statusCode": statusCode,
        "body": body
    }
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
    user_id = event['pathParameters']['user_id']
    order_id = str(uuid.uuid4())

    try:
        response = orders_table.put_item(
            Item = {
                'id': order_id, 
                'paid': False,
                'items': [],
                'user_id': user_id,
                'total_cost': decimal.Decimal('0.0')
            }
        )
        res = str(json.dumps(response, default=str))
        statusCode = 200
        body = json.dumps({
            'order_id': order_id
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
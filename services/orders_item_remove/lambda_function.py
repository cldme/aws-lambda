import os
import json
import uuid
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# get the service resource
dynamodb = boto3.resource('dynamodb')
# get the users table
ORDERS_TABLE = os.environ['ORDERS_TABLE']
STOCK_TABLE = os.environ['STOCK_TABLE']

# helper class to convert a DynamoDB item to JSON
# for details see: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.03.html
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def lambda_handler(event, context):
    
    orders_table = dynamodb.Table(ORDERS_TABLE)
    stock_table = dynamodb.Table(STOCK_TABLE)
    order_id = event['pathParameters']['order_id']
    item_id = event['pathParameters']['item_id']

    try:
        order_object = orders_table.get_item(Key={'id': order_id})
        stock_object = stock_table.get_item(Key={'id': item_id})
        order_items = order_object['Item']['items']
        order_items.remove(item_id)

        print(f'get_item order result: {str(json.dumps(order_object, cls=DecimalEncoder))}')
        print(f'get_item stock result: {str(json.dumps(stock_object, cls=DecimalEncoder))}')

        response = orders_table.update_item(
            Key={'id': order_id},
            UpdateExpression="set #tms = :items",
            ExpressionAttributeValues={':items': order_items},
            ExpressionAttributeNames={'#tms': 'items'},
            ReturnValues="UPDATED_NEW"
        )
        res = str(json.dumps(response, cls=DecimalEncoder))
        print(f'item successfully added to order: {res}')

        statusCode = 200
    except ClientError as e:
        print(f'get_item error: {e}')
        statusCode = 400
    except ValueError as e:
        print(f'get_item error (item does not exist in list): {e}')
        statusCode = 400

    return {
        "statusCode": statusCode
    }
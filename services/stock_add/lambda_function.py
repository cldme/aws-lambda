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
    
    stock_table = dynamodb.Table(STOCK_TABLE)
    item_id = event['pathParameters']['item_id']
    amount = decimal.Decimal(event['pathParameters']['number'])

    try:
        stock_object = stock_table.get_item(Key={'id': item_id})
        current_stock = stock_object['Item']['stock']
        new_stock = current_stock + amount

        response = stock_table.update_item(
            Key={'id': item_id},
            UpdateExpression="set stock = :stock",
            ExpressionAttributeValues={':stock': decimal.Decimal(new_stock)},
            ReturnValues="UPDATED_NEW"
        )
        res = str(json.dumps(response, cls=DecimalEncoder))
        print(f'stock successfully added: {res}')
        statusCode = 200
    except ClientError as e:
        print(f'update_item error: {e}')
        statusCode = 400

    return {
        "statusCode": statusCode
    }
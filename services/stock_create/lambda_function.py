import os
import json
import uuid
import boto3
import decimal
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
        res = str(json.dumps(response, cls=DecimalEncoder))
        statusCode = 200
        body = json.dumps({
            'item_id': item_id
        })
        print(f'put_item result: {res}')
    except ClientError as e:
        statusCode = 400
        body = json.dumps({})
        print(f'put_item error: {e}')

    return {
        "statusCode": statusCode,
        "body": body
    }
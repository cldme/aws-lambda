import os
import json
import uuid
import boto3
import decimal
from botocore.exceptions import ClientError

# get the service resource
dynamodb = boto3.resource('dynamodb')
# get the users table
ORDERS_TABLE = os.environ['ORDERS_TABLE']

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
    order_id = event['pathParameters']['order_id']

    try:
        response = orders_table.delete_item(Key={'id': order_id})
        res = str(json.dumps(response, cls=DecimalEncoder))
        print(f'order successfully removed: {res}')
        statusCode = 200
    except ClientError as e:
        print(f'delete_item error: {e}')
        statusCode = 400

    return {
        "statusCode": statusCode
    }
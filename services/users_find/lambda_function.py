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
USERS_TABLE = os.environ['USERS_TABLE']

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
    
    users_table = dynamodb.Table(USERS_TABLE)
    user_id = event['pathParameters']['user_id']

    try:
        response = users_table.get_item(Key={'id': user_id})
        res = str(json.dumps(response, cls=DecimalEncoder))
        item = response['Item']
        print(f'get_item result: {res}')
        statusCode = 200
        body = json.dumps({
            'user_id': item['id'],
            'credit': item['credit']
        }, cls=DecimalEncoder)
    except ClientError as e:
        print(f'get_item error: {e}')
        statusCode = 400
        body = json.dumps({})

    return {
        "statusCode": statusCode,
        "body": body
    }
import os
import json
import uuid
import boto3
import decimal
import requests
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')

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

    # This will produce an error for a test on the lambda function itself, but not if it is tested API wise
    if event['httpMethod'] == "DELETE":
        users_table = dynamodb.Table('users_table')
        user_id = event['pathParameters']['user_id']

        try:
            response = users_table.delete_item(Key={'id': user_id})
        except ClientError as e:
            print(e.response['Error']['Message'])
            statusCode = 400
            body = json.dumps({})
        else:
            item = response['Item']
            print("User successfully fetched from DynamoDB")
            print(json.dumps(response, indent=4, cls=DecimalEncoder))

            statusCode = 200
            body = json.dumps({
                'user_id': item['id'],
                'credit': item['credit']
            }) 

    return {
        "statusCode": statusCode,
        "body": body
    }
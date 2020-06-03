import decimal
import json
import os

import boto3

# get the service resource
dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table(os.environ['USERS_TABLE'])


def lambda_handler(event, context):
    user_id = event['pathParameters']['user_id']
    amount = decimal.Decimal(event['pathParameters']['amount'])

    try:
        response = users_table.update_item(
            Key={'id': user_id},
            UpdateExpression="set credit = credit - :amount",
            ConditionExpression="credit >= :amount",
            ExpressionAttributeValues={':amount': amount},
            ReturnValues="UPDATED_NEW"
        )
        res = json.dumps(response, default=str)
        print(f'credit successfully subtracted: {res}')
        status_code = 200
    except Exception as e:
        print(f'update_item error: {e}')
        status_code = 400

    return {
        "statusCode": status_code
    }

import decimal
import json
import os
import uuid

import boto3

# get the service resource
dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table(os.environ['USERS_TABLE'])


def lambda_handler(event, context):
    user_id = str(uuid.uuid4())

    try:
        response = users_table.put_item(Item={'id': user_id, 'credit': decimal.Decimal('0.0')})
        res = json.dumps(response, default=str)
        status_code = 200
        body = json.dumps({
            'user_id': user_id
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

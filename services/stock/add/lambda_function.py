import json
import os

import boto3

# get the service resource
dynamodb = boto3.resource('dynamodb')
stock_table = dynamodb.Table(os.environ['STOCK_TABLE'])


def lambda_handler(event, context):
    item_id = event['pathParameters']['item_id']
    amount = int(event['pathParameters']['number'])

    print(f'stock_add: {item_id} {amount}')

    try:
        response = stock_table.update_item(
            Key={'id': item_id},
            UpdateExpression="set stock = stock + :amount",
            ConditionExpression="stock >= :negativeAmount",
            ExpressionAttributeValues={
                ':amount': amount,
                ':negativeAmount': -amount
            },
            ReturnValues="UPDATED_NEW"
        )
        res = json.dumps(response, default=str)
        print(f'stock successfully added: {res}')
        status_code = 200
    except Exception as e:
        print(f'update_item error: {e}')
        status_code = 400

    return {
        "statusCode": status_code
    }

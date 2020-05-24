import os
import json
import uuid
import boto3
import decimal

# get the service resource
dynamodb = boto3.resource('dynamodb')
# get the users table
STOCK_TABLE = os.environ['STOCK_TABLE']

def lambda_handler(event, context):
    
    stock_table = dynamodb.Table(STOCK_TABLE)
    item_id = event['pathParameters']['item_id']
    amount = decimal.Decimal(event['pathParameters']['number'])

    try:
        stock_object = stock_table.get_item(Key={'id': item_id})
        current_stock = stock_object['Item']['stock']
        new_stock = current_stock - amount
        if new_stock > 0:
            response = stock_table.update_item(
                Key={'id': item_id},
                UpdateExpression="set stock = :stock",
                ExpressionAttributeValues={':stock': decimal.Decimal(new_stock)},
                ReturnValues="UPDATED_NEW"
            )
            res = json.dumps(response, default=str)
            print(f'stock successfully subtracted: {res}')
            statusCode = 200
        else:
            statusCode = 400
    except Exception as e:
        print(f'update_item error: {e}')
        statusCode = 400

    return {
        "statusCode": statusCode
    }
import os
import json
import uuid
import boto3
import decimal

# get the service resource
dynamodb = boto3.resource('dynamodb')
# get the users table
ORDERS_TABLE = os.environ['ORDERS_TABLE']
STOCK_TABLE = os.environ['STOCK_TABLE']

def lambda_handler(event, context):
    
    orders_table = dynamodb.Table(ORDERS_TABLE)
    stock_table = dynamodb.Table(STOCK_TABLE)
    order_id = event['pathParameters']['order_id']
    item_id = event['pathParameters']['item_id']

    try:
        order_object = orders_table.get_item(Key={'id': order_id})
        stock_object = stock_table.get_item(Key={'id': item_id})
        order_items = order_object['Item']['items']
        total_cost = order_object['Item']['total_cost'] + stock_object['Item']['price']
        order_items.append(item_id)

        print(f'get_item order result: {str(json.dumps(order_object, default=str))}')
        print(f'get_item stock result: {str(json.dumps(stock_object, default=str))}')

        response = orders_table.update_item(
            Key={'id': order_id},
            UpdateExpression="SET #items = :items, #cost = :cost",
            ExpressionAttributeValues={
                ':items': order_items,
                ':cost': total_cost
            },
            ExpressionAttributeNames={
                '#items': 'items',
                '#cost': 'total_cost'
            },
            ReturnValues="UPDATED_NEW"
        )
        res = json.dumps(response, default=str)
        print(f'item successfully added to order: {res}')

        statusCode = 200
    except Exception as e:
        print(f'get_item error: {e}')
        statusCode = 400

    return {
        "statusCode": statusCode
    }
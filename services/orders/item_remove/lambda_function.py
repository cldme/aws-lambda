import decimal
import json
import os

import boto3

# get the service resource
dynamodb = boto3.resource('dynamodb')
client = boto3.client('lambda')
orders_table = dynamodb.Table(os.environ['ORDERS_TABLE'])


# invoke lambda function with given name and payload
def invoke_lambda(name, payload, invocation_type='RequestResponse'):
    print(f'invoking lambda function: {name}')
    payload = json.dumps(payload)

    res = client.invoke(
        FunctionName=name,
        InvocationType=invocation_type,
        LogType='Tail',
        Payload=bytes(payload, encoding='utf8')
    )

    return res


# get stock
def get_stock(item_id):
    payload = {
        'pathParameters': {
            'item_id': item_id
        }
    }
    res = invoke_lambda('stock_find_lambda', payload)
    # get result object from lambda call
    res = json.loads(res['Payload'].read())
    print(f'stock service result: {res}')
    return json.loads(res['body'])


def lambda_handler(event, context):
    order_id = event['pathParameters']['order_id']
    item_id = event['pathParameters']['item_id']

    try:
        # get stock object via stock service
        stock_object = get_stock(item_id)

        print(f'get_item stock result: {str(json.dumps(stock_object, default=str))}')

        response = orders_table.update_item(
            Key={'id': order_id},
            UpdateExpression="ADD #items.#item_id :quantity SET #cost = #cost - :price",
            ConditionExpression="attribute_exists(#items.#item_id) AND #items.#item_id > :zero",
            ExpressionAttributeValues={
                ':quantity': -1,
                ':price': decimal.Decimal(stock_object['price']),
                ':zero': 0
            },
            ExpressionAttributeNames={
                '#items': 'items',
                '#item_id': item_id,
                '#cost': 'total_cost'
            },
            ReturnValues="UPDATED_NEW"
        )
        res = json.dumps(response, default=str)
        print(f'item successfully removed from order: {res}')

        status_code = 200
    except ValueError as e:
        print(f'get_item error (item does not exist in list): {e}')
        status_code = 400
    except Exception as e:
        print(f'get_item error: {e}')
        status_code = 400

    return {
        "statusCode": status_code
    }

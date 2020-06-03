import decimal
import json
import os

import boto3

ORDERS_TABLE = os.environ['ORDERS_TABLE']
USERS_TABLE = os.environ['USERS_TABLE']

dynamodb = boto3.resource('dynamodb')
orders_table = dynamodb.Table(ORDERS_TABLE)


def get_order(order_id):
    """Obtain the order by the given id."""
    response = orders_table.get_item(Key={'id': order_id})
    return response['Item']


def pay_order(order):
    """Mark the specified order as paid and subtract the costs from the user's credit."""
    dynamodb.meta.client.transact_write_items(
        TransactItems=[
            {
                'Update': {
                    'TableName': ORDERS_TABLE,
                    'Key': {'id': order['id']},
                    'UpdateExpression': 'SET paid = :paid',
                    'ConditionExpression': 'paid = :previousPaid',
                    'ExpressionAttributeValues': {
                        ':paid': True,
                        ':previousPaid': False,
                    },
                },

            },
            {
                'Update': {
                    'TableName': USERS_TABLE,
                    'Key': {'id': order['user_id']},
                    'UpdateExpression': 'SET credit = credit - :cost',
                    'ConditionExpression': 'credit >= :cost',
                    'ExpressionAttributeValues': {
                        ':cost': order['total_cost'],
                    }
                }
            }
        ]
    )


def lambda_handler(event, context):
    order_id = event['pathParameters']['order_id']
    amount = decimal.Decimal(event['pathParameters']['amount'])

    try:
        order = get_order(order_id)

        if order['total_cost'] != amount:
            raise ValueError("The amount does not cover the total costs of the order")

        if not order['paid']:
            pay_order(order)

        status_code = 200
        body = json.dumps({})
    except Exception as e:
        print(f'status error: {e}')
        status_code = 400
        body = json.dumps({})

    return {
        "statusCode": status_code,
        "body": body
    }

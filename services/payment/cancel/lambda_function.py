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


def revert_order(order):
    """Revert the specified order and add the costs back to the user's credit."""
    dynamodb.meta.client.transact_write_items(
        TransactItems=[
            {
                'Update': {
                    'TableName': ORDERS_TABLE,
                    'Key': {'id': order['id']},
                    'UpdateExpression': 'SET paid = :paid',
                    'ConditionExpression': 'paid = :previousPaid',
                    'ExpressionAttributeValues': {
                        ':paid': False,
                        ':previousPaid': True,
                    },
                },

            },
            {
                'Update': {
                    'TableName': USERS_TABLE,
                    'Key': {'id': order['user_id']},
                    'UpdateExpression': 'SET credit = credit + :cost',
                    'ExpressionAttributeValues': {
                        ':cost': order['total_cost'],
                    }
                }
            }
        ]
    )


def lambda_handler(event, context):
    order_id = event['pathParameters']['order_id']

    print(f'payment_cancel: {order_id}')

    try:
        order = get_order(order_id)

        if not order['paid']:
            raise ValueError("The order has not been paid yet")

        revert_order(order)

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

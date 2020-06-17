import os
import json
import boto3
import decimal

# get the service resource
aws_lambda = boto3.client('lambda')
dynamodb = boto3.resource('dynamodb')
orders_table = dynamodb.Table(os.environ['ORDERS_TABLE'])


# invoke lambda function with given name and payload
def invoke_lambda(name, payload, invocation_type='RequestResponse'):
    print(f'invoking lambda function: {name}')
    payload = json.dumps(payload)

    res = aws_lambda.invoke(
        FunctionName=name,
        InvocationType=invocation_type,
        LogType='Tail',
        Payload=bytes(payload, encoding='utf8')
    )

    return res


# make payment
def make_payment(order):
    print(f'making payment via calling the payment service')
    payload = {
        'pathParameters': {
            'user_id': order['user_id'],
            'order_id': order['id'],
            'amount': str(order['total_cost'])
        }
    }
    res = invoke_lambda('payment_pay_lambda', payload)
    # get result object from lambda call
    res = json.loads(res['Payload'].read())
    print(f'payment service result: {res}')

    if res['statusCode'] != 200:
        raise ValueError('error thrown while making the payment')


# subtract stock
def subtract_stock(order):
    print(f'subtract stock via calling the stock service')
    items = order['items']
    # keep track of the items that were updated (used for rollback in case of failure)
    queue = list()
    for item in items:
        payload = {
            'pathParameters': {
                'item_id': item,
                'number': str(items[item])
            }
        }
        res = invoke_lambda('stock_subtract_lambda', payload)
        # get result object from lambda call
        res = json.loads(res['Payload'].read())
        print(f'stock subtract service result: {res}')

        # in case of failure rollback previous actions
        if res['statusCode'] != 200:
            print(f'failed updating stock with result: {res}')
            print(f'rolling back now!')
            # rollback user's payment
            payload = {
                'pathParameters': {
                    'user_id': order['user_id'],
                    'order_id': order['id']
                }
            }
            # invoke async lambda (no need to wait for results here)
            res = invoke_lambda('payment_cancel_lambda', payload, 'Event')
            # rollback stock subtractions
            for q in queue:
                # invoke async lambda (no need to wait for results here)
                res = invoke_lambda('stock_add_lambda', q, 'Event')
            # exit after rollback is complete
            raise ValueError('error while updating the stock! rollback complete!')

        print(f'subtracted stock for item: {item} with result: {res}')
        # in case of success add item to done queue
        queue.append(payload)


def lambda_handler(event, context):
    order_id = event['pathParameters']['order_id']

    try:
        res = orders_table.get_item(Key={'id': order_id})
        order = res['Item']

        # make the payment via calling the payment service
        make_payment(order)

        print(f'done making the payment!')

        # subtract the stock via calling the stock service
        subtract_stock(order)

        print(f'done updating all stock!')

        status_code = 200
    except Exception as e:
        status_code = 400
        print(f'checkout error: {e}')

    return {
        "statusCode": status_code
    }

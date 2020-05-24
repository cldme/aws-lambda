import os
import json
import boto3
import decimal

# get the service resource
dynamodb = boto3.resource('dynamodb')
# get the users table
ORDERS_TABLE = os.environ['ORDERS_TABLE']

# invoke lambda function with given name and payload
def invoke_lambda(name, payload, invocation_type='RequestResponse'):
    print(f'invoking lambda function: {name}')
    client = boto3.client('lambda')
    payload = json.dumps(payload)
    
    res = client.invoke(
        FunctionName=name,
        InvocationType=invocation_type,
        LogType='Tail',
        Payload=bytes(payload, encoding='utf8')
    )

    return res

def lambda_handler(event, context):
    
    orders_table = dynamodb.Table(ORDERS_TABLE)
    order_id = event['pathParameters']['order_id']

    try:
        res = orders_table.get_item(Key={'id': order_id})
        order = res['Item']

        # make the payment via calling the payment service
        print(f'making payment via calling the payment service')
        payload = {
            'pathParameters': {
                'order_id': order_id,
                'amount': str(order['total_cost'])
            }
        }
        res = invoke_lambda('payment_pay_lambda', payload)

        if res['StatusCode'] != 200:
            raise ValueError('error thrown while making the payment | status: ' + res['StatusCode'])

        print(f'done making the payment with result: {res}')

        # subtract the stock via calling the stock service
        print(f'subtract stock via calling the stock service')
        items = order['items']
        # keep track of the items that were updated (used for rollback in case of failure)
        queue = list()
        for item in items:
            payload = {
                'pathParameters': {
                    'item_id': item,
                    'number': '1'
                }
            }
            res = invoke_lambda('stock_subtract_lambda', payload)

            # in case of failure rollback previous actions
            if res['StatusCode'] != 200:
                print(f'failed updating stock with result: {res}')
                print(f'rolling back now!')
                # TODO: rollback user's payment
                for q in queue:
                    # invoke async lambda (no need to wait for results here)
                    res = invoke_lambda('stock_add_lambda', q, 'Event')
                # exit after rollback is complete
                raise ValueError('error while updating the stock! rollback complete!')
            
            print(f'subtracted stock for item: {item} with result: {res}')
            # in case of success add item to done queue
            queue.append(payload)

        print(f'done updating all stock!')

        statusCode = 200
    except Exception as e:
        statusCode = 400
        print(f'checkout error: {e}')

    return {
        "statusCode": statusCode
    }
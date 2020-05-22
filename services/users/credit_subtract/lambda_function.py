import os
import json
import uuid
import boto3
import decimal

# get the service resource
dynamodb = boto3.resource('dynamodb')
# get the users table
USERS_TABLE = os.environ['USERS_TABLE']

def lambda_handler(event, context):

    users_table = dynamodb.Table(USERS_TABLE)
    user_id = event['pathParameters']['user_id']
    amount = decimal.Decimal(event['pathParameters']['amount'])

    try:
        user_object = users_table.get_item(Key={'id': user_id})
        current_credit = user_object['Item']['credit']
        new_credit = current_credit - amount

        if new_credit < 0:
            raise ValueError('user credit can not be negative!')

        response = users_table.update_item(
            Key={'id': user_id},
            UpdateExpression="set credit = :credit",
            ExpressionAttributeValues={':credit': decimal.Decimal(new_credit)},
            ReturnValues="UPDATED_NEW"
        )
        res = json.dumps(response, default=str)
        print(f'credit successfully subtracted: {res}')
        statusCode = 200
    except Exception as e:
        print(f'update_item error: {e}')
        statusCode = 400

    return {
        "statusCode": statusCode
    }
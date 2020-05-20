import os
import json
import uuid
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# get the service resource
dynamodb = boto3.resource('dynamodb')
# get the users table
USERS_TABLE = os.environ['USERS_TABLE']

# helper class to convert a DynamoDB item to JSON
# for details see: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.03.html
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def lambda_handler(event, context):

    users_table = dynamodb.Table(USERS_TABLE)
    user_id = event['pathParameters']['user_id']
    amount = decimal.Decimal(event['pathParameters']['amount'])

    try:
        user_object = users_table.get_item(Key={'id': user_id})
        current_credit = user_object['Item']['credit']
        new_credit = current_credit - amount
        
        response = users_table.update_item(
            Key={'id': user_id},
            UpdateExpression="set credit = :credit",
            ExpressionAttributeValues={':credit': decimal.Decimal(new_credit)},
            ReturnValues="UPDATED_NEW"
        )
        res = str(json.dumps(response, cls=DecimalEncoder))
        print(f'credit successfully subtracted: {res}')
        statusCode = 200
    except ClientError as e:
        print(f'update_item error: {e}')
        statusCode = 400

    return {
        "statusCode": statusCode
    }
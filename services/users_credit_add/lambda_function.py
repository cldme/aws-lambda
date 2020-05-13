import os
import json
import uuid
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# get the service resource
dynamodb = boto3.resource('dynamodb')

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

    if event['httpMethod'] == "POST":
        users_table = dynamodb.Table('users_table')
        user_id = event['pathParameters']['user_id']
        amount = decimal.Decimal(event['pathParameters']['amount'])

        ## build-in mechanism against negative credit

        try:
            user_object = users_table.get_item(Key={'id': user_id})
            current_credit = user_object['Item']['credit']
            new_credit = current_credit+amount

            response = users_table.update_item(
                Key={'id': user_id},
                UpdateExpression="set credit = :credit",
                ExpressionAttributeValues={':credit': decimal.Decimal(new_credit)},
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            statusCode = 400
        else:
            print(f'Credit successfully added!')
            statusCode = 200

    return {
        "statusCode": statusCode
    }
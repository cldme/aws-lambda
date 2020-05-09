import os
import json
import uuid
import boto3
import decimal

# get the service resource
dynamodb = boto3.resource('dynamodb')

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

    # generate new random user id for user
    # use UUID4 for details see: https://pynative.com/python-uuid-module-to-generate-universally-unique-identifiers/
    user_id = str(uuid.uuid4())

    # get the user table
    users_table = dynamodb.Table(USERS_TABLE)

    # put item into table
    response = users_table.put_item(
        Item = {
            'id': user_id
        }
    )

    res = str(json.dumps(response, cls=DecimalEncoder))
    print(f'put_item result: {res}')

    return {
        "statusCode": 200,
        "body": json.dumps({
            "id": user_id
        }),
    }
import json

def lambda_handler(event, context):

    body            = event['body']
    resource        = event['resource']
    path            = event['path']
    method          = event['httpMethod']
    headers         = event['headers']
    query_params    = event['queryStringParameters']
    path_params     = event['pathParameters']
    time            = event['requestContext']['requestTime']

    print(f'event: {event}')

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            "body": body,
            "resource": resource,
            "path": path,
            "method": method,
            "query_params": query_params,
            "path_params": path_params,
            "time": time
        }),
    }
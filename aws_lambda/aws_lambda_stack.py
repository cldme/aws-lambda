from aws_cdk import core
from aws_cdk import aws_dynamodb
from aws_cdk import aws_lambda

class AwsLambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        table = aws_dynamodb.Table(
            self, 
            'table_1',
            partition_key=aws_dynamodb.Attribute(
                name='id',
                type=aws_dynamodb.AttributeType.STRING
            ),
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST
        )

        hello_lambda = aws_lambda.Function(
            self, 
            'hello_lambda_function',
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler='lambda_function.lambda_handler',
            code=aws_lambda.Code.asset('./services/hello')
        )

        table.grant_read_write_data(hello_lambda)

from pathlib import Path
from aws_cdk import core
from aws_cdk import aws_lambda
from aws_cdk import aws_dynamodb
from aws_cdk import aws_apigateway
from aws_cdk_lambda_asset.zip_asset_code import ZipAssetCode

class AwsLambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        work_dir = Path(__file__).parents[1]

        # The code that defines your stack goes here

        # DynamoDB
        table = aws_dynamodb.Table(
            self, 
            "table_1",
            partition_key=aws_dynamodb.Attribute(
                name="id",
                type=aws_dynamodb.AttributeType.STRING
            ),
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
            table_name="table_1"
        )

        # Lambdas
        items_lambda = aws_lambda.Function(
            self,
            "items_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/items"),
            function_name="items_lambda"
        )

        users_create_lambda = aws_lambda.Function(
            self,
            "users_create_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="users_create/lambda_function.lambda_handler",
            code=ZipAssetCode(work_dir=work_dir, include=["./services/users_create"], file_name="users_create_lambda.zip"),
            function_name="users_create_lambda"
        )

        # API Lambda Integrations
        items_integration = aws_apigateway.LambdaIntegration(items_lambda)
        users_integration = aws_apigateway.LambdaIntegration(users_create_lambda)

        # REST API
        api = aws_apigateway.RestApi(self, "webshop-api", rest_api_name="webshop-api")

        items = api.root.add_resource("items")
        item = items.add_resource("{item}")
        item.add_method("GET", items_integration)       # GET   /items/{item}
        items.add_method("GET", items_integration)      # GET   /items
        items.add_method("POST", items_integration)     # POST  /items

        users = api.root.add_resource("users")
        user = users.add_resource("{user}")
        user.add_method("GET", users_integration)       # GET   /users/{user}
        users.add_method("GET", users_integration)      # GET   /users
        users.add_method("POST", users_integration)     # POST  /users

        # Permissions
        table.grant_read_write_data(items_lambda)
        table.grant_read_write_data(users_create_lambda)
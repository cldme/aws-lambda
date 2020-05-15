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

        # DynamoDB tables
        users_table = aws_dynamodb.Table(
            self, 
            "users_table",
            partition_key=aws_dynamodb.Attribute(
                name="id",
                type=aws_dynamodb.AttributeType.STRING
            ),
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
            table_name="users_table"
        )

        orders_table = aws_dynamodb.Table(
            self, 
            "orders_table",
            partition_key=aws_dynamodb.Attribute(
                name="id",
                type=aws_dynamodb.AttributeType.STRING
            ),
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
            table_name="orders_table"
        )

        # Lambdas
        users_create_lambda = aws_lambda.Function(
            self,
            "users_create_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            # handler="users_create/lambda_function.lambda_handler",
            # code=ZipAssetCode(work_dir=work_dir, include=["./services/users_create"], file_name="users_create_lambda.zip"),
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/users_create"),
            function_name="users_create_lambda"
        )

        users_find_lambda = aws_lambda.Function(
            self,
            "users_find_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            # handler="users_find/lambda_function.lambda_handler",
            # code=ZipAssetCode(work_dir=work_dir, include=["./services/users_find"], file_name="users_find_lambda.zip"),
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/users_find"),
            function_name="users_find_lambda"
        )

        users_remove_lambda = aws_lambda.Function(
            self,
            "users_remove_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            # handler="users_remove/lambda_function.lambda_handler",
            # code=ZipAssetCode(work_dir=work_dir, include=["./services/users_remove"], file_name="users_remove_lambda.zip"),
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/users_remove"),
            function_name="users_remove_lambda"
        )

        users_credit_subtract_lambda = aws_lambda.Function(
            self,
            "users_credit_subtract_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            # handler="users_credit_subtract/lambda_function.lambda_handler",
            # code=ZipAssetCode(work_dir=work_dir, include=["./services/users_credit_subtract"], file_name="users_credit_subtract_lambda.zip"),
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/users_credit_subtract"),
            function_name="users_credit_subtract_lambda"
        )

        users_credit_add_lambda = aws_lambda.Function(
            self,
            "users_credit_add_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            # handler="users_credit_add/lambda_function.lambda_handler",
            # code=ZipAssetCode(work_dir=work_dir, include=["./services/users_credit_add"], file_name="users_credit_add_lambda.zip"),
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/users_credit_add"),
            function_name="users_credit_add_lambda"
        )

        orders_create_lambda = aws_lambda.Function(
            self,
            "orders_create_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            # handler="orders_create/lambda_function.lambda_handler",
            # code=ZipAssetCode(work_dir=work_dir, include=["./services/orders_create"], file_name="orders_create_lambda.zip"),
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/orders_create"),
            function_name="orders_create_lambda"
        )

        orders_remove_lambda = aws_lambda.Function(
            self,
            "orders_remove_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            # handler="orders_create/lambda_function.lambda_handler",
            # code=ZipAssetCode(work_dir=work_dir, include=["./services/orders_create"], file_name="orders_create_lambda.zip"),
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/orders_remove"),
            function_name="orders_remove_lambda"
        )

        # API Lambda integrations
        users_create_integration = aws_apigateway.LambdaIntegration(users_create_lambda)
        users_find_integration = aws_apigateway.LambdaIntegration(users_find_lambda)
        users_remove_integration = aws_apigateway.LambdaIntegration(users_remove_lambda)
        users_credit_subtract_integration = aws_apigateway.LambdaIntegration(users_credit_subtract_lambda)
        users_credit_add_integration = aws_apigateway.LambdaIntegration(users_credit_add_lambda)

        orders_create_integration = aws_apigateway.LambdaIntegration(orders_create_lambda)
        orders_remove_integration = aws_apigateway.LambdaIntegration(orders_remove_lambda)

        # REST API
        api = aws_apigateway.RestApi(self, "webshop-api", rest_api_name="webshop-api")

        # USERS RESOURCE
        users = api.root.add_resource("users")
        users_credit = users.add_resource("credit")

        # POST /users/create
        users_create = users.add_resource("create")
        users_create.add_method("POST", users_create_integration)

        # DELETE /users/remove/{user_id}
        users_remove = users.add_resource("remove").add_resource("{user_id}")
        users_remove.add_method("DELETE", users_remove_integration)

        # FIND /users/find/{user_id}
        users_find = users.add_resource("find").add_resource("{user_id}")
        users_find.add_method("GET", users_find_integration)

        # POST /users/credit/subtract/{user_id}/{amount}
        users_credit_subtract = users_credit.add_resource("subtract").add_resource("{user_id}").add_resource("{amount}")
        users_credit_subtract.add_method("POST", users_credit_subtract_integration)

        # POST /users/credit/add/{user_id}/{amount}
        users_credit_add = users_credit.add_resource("add").add_resource("{user_id}").add_resource("{amount}")
        users_credit_add.add_method("POST", users_credit_add_integration)

        # ORDERS RESOURCE
        orders = api.root.add_resource("orders")

        # POST /orders/create/{user_id}
        orders_create = orders.add_resource("create").add_resource("{user_id}")
        orders_create.add_method("POST", orders_create_integration)

        # DELETE /orders/remove/{order_id}
        orders_remove = orders.add_resource("remove").add_resource("{order_id}")
        orders_remove.add_method("DELETE", orders_remove_integration)
        
        # Permissions
        users_table.grant_read_write_data(users_create_lambda)
        users_table.grant_read_write_data(users_find_lambda)
        users_table.grant_read_write_data(users_remove_lambda)
        users_table.grant_read_write_data(users_credit_subtract_lambda)
        users_table.grant_read_write_data(users_credit_add_lambda)

        orders_table.grant_read_write_data(orders_create_lambda)
        orders_table.grant_read_write_data(orders_remove_lambda)

        # Environment variables
        users_create_lambda.add_environment("USERS_TABLE", users_table.table_name)
        users_remove_lambda.add_environment("USERS_TABLE", users_table.table_name)
        users_find_lambda.add_environment("USERS_TABLE", users_table.table_name)
        users_credit_subtract_lambda.add_environment("USERS_TABLE", users_table.table_name)
        users_credit_add_lambda.add_environment("USERS_TABLE", users_table.table_name)

        orders_create_lambda.add_environment("ORDERS_TABLE", orders_table.table_name)
        orders_remove_lambda.add_environment("ORDERS_TABLE", orders_table.table_name)
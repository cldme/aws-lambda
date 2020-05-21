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
            table_name="users_table",
            removal_policy=core.RemovalPolicy.DESTROY
        )

        orders_table = aws_dynamodb.Table(
            self, 
            "orders_table",
            partition_key=aws_dynamodb.Attribute(
                name="id",
                type=aws_dynamodb.AttributeType.STRING
            ),
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
            table_name="orders_table",
            removal_policy=core.RemovalPolicy.DESTROY
        )

        stock_table = aws_dynamodb.Table(
            self, 
            "stock_table",
            partition_key=aws_dynamodb.Attribute(
                name="id",
                type=aws_dynamodb.AttributeType.STRING
            ),
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
            table_name="stock_table",
            removal_policy=core.RemovalPolicy.DESTROY
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
            # handler="orders_remove/lambda_function.lambda_handler",
            # code=ZipAssetCode(work_dir=work_dir, include=["./services/orders_remove"], file_name="orders_remove_lambda.zip"),
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/orders_remove"),
            function_name="orders_remove_lambda"
        )

        orders_find_lambda = aws_lambda.Function(
            self,
            "orders_find_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            # handler="orders_find/lambda_function.lambda_handler",
            # code=ZipAssetCode(work_dir=work_dir, include=["./services/orders_find"], file_name="orders_find_lambda.zip"),
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/orders_find"),
            function_name="orders_find_lambda"
        )

        orders_item_add_lambda = aws_lambda.Function(
            self,
            "orders_item_add_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            # handler="orders_item_add/lambda_function.lambda_handler",
            # code=ZipAssetCode(work_dir=work_dir, include=["./services/orders_item_add"], file_name="orders_item_add_lambda.zip"),
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/orders_item_add"),
            function_name="orders_item_add_lambda"
        )

        orders_item_remove_lambda = aws_lambda.Function(
            self,
            "orders_item_remove_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            # handler="orders_item_remove/lambda_function.lambda_handler",
            # code=ZipAssetCode(work_dir=work_dir, include=["./services/orders_item_remove"], file_name="orders_item_remove_lambda.zip"),
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/orders_item_remove"),
            function_name="orders_item_remove_lambda"
        )

        stock_create_lambda = aws_lambda.Function(
            self,
            "stock_create_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            # handler="stock_create/lambda_function.lambda_handler",
            # code=ZipAssetCode(work_dir=work_dir, include=["./services/stock_create"], file_name="stock_create_lambda.zip"),
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/stock_create"),
            function_name="stock_create_lambda"
        )

        stock_find_lambda = aws_lambda.Function(
            self,
            "stock_find_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            # handler="stock_find/lambda_function.lambda_handler",
            # code=ZipAssetCode(work_dir=work_dir, include=["./services/stock_find"], file_name="stock_find_lambda.zip"),
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/stock_find"),
            function_name="stock_find_lambda"
        )

        stock_add_lambda = aws_lambda.Function(
            self,
            "stock_add_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            # handler="stock_add/lambda_function.lambda_handler",
            # code=ZipAssetCode(work_dir=work_dir, include=["./services/stock_add"], file_name="stock_add_lambda.zip"),
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/stock_add"),
            function_name="stock_add_lambda"
        )

        stock_subtract_lambda = aws_lambda.Function(
            self,
            "stock_subtract_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            # handler="stock_subtract/lambda_function.lambda_handler",
            # code=ZipAssetCode(work_dir=work_dir, include=["./services/stock_subtract"], file_name="stock_subtract_lambda.zip"),
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/stock_subtract"),
            function_name="stock_subtract_lambda"
        )

        payment_status_lambda = aws_lambda.Function(
            self,
            "payment_status_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/payment_status"),
            function_name="payment_status_lambda"
        )

        payment_pay_lambda = aws_lambda.Function(
            self,
            "payment_pay_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/payment_pay"),
            function_name="payment_pay_lambda"
        )

        payment_cancel_lambda = aws_lambda.Function(
            self,
            "payment_cancel_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/payment_cancel"),
            function_name="payment_cancel_lambda"
        )

        # API Lambda integrations
        users_create_integration = aws_apigateway.LambdaIntegration(users_create_lambda)
        users_find_integration = aws_apigateway.LambdaIntegration(users_find_lambda)
        users_remove_integration = aws_apigateway.LambdaIntegration(users_remove_lambda)
        users_credit_subtract_integration = aws_apigateway.LambdaIntegration(users_credit_subtract_lambda)
        users_credit_add_integration = aws_apigateway.LambdaIntegration(users_credit_add_lambda)

        orders_create_integration = aws_apigateway.LambdaIntegration(orders_create_lambda)
        orders_remove_integration = aws_apigateway.LambdaIntegration(orders_remove_lambda)
        orders_find_integration = aws_apigateway.LambdaIntegration(orders_find_lambda)
        orders_item_add_integration = aws_apigateway.LambdaIntegration(orders_item_add_lambda)
        orders_item_remove_integration = aws_apigateway.LambdaIntegration(orders_item_remove_lambda)

        stock_create_integration = aws_apigateway.LambdaIntegration(stock_create_lambda)
        stock_find_integration = aws_apigateway.LambdaIntegration(stock_find_lambda)
        stock_add_integration = aws_apigateway.LambdaIntegration(stock_add_lambda)
        stock_subtract_integration = aws_apigateway.LambdaIntegration(stock_subtract_lambda)

        payment_status_integration = aws_apigateway.LambdaIntegration(payment_status_lambda)
        payment_pay_integration = aws_apigateway.LambdaIntegration(payment_pay_lambda)
        payment_cancel_integration = aws_apigateway.LambdaIntegration(payment_cancel_lambda)

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

        # GET /users/find/{user_id}
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

        # GET /orders/find/{order_id}
        orders_find = orders.add_resource("find").add_resource("{order_id}")
        orders_find.add_method("GET", orders_find_integration)

        # POST /orders/addItem/{order_id}/{item_id}
        orders_item_add = orders.add_resource("addItem").add_resource("{order_id}").add_resource("{item_id}")
        orders_item_add.add_method("POST", orders_item_add_integration)

        # DELETE /orders/removeItem/{order_id}/{item_id}
        orders_item_remove = orders.add_resource("removeItem").add_resource("{order_id}").add_resource("{item_id}")
        orders_item_remove.add_method("DELETE", orders_item_remove_integration)

        # STOCK RESOURCE
        stock = api.root.add_resource("stock")

        # POST /stock/item/create/{price}
        stock_create = stock.add_resource("item").add_resource("create").add_resource("{price}")
        stock_create.add_method("POST", stock_create_integration)

        # GET /stock/find/{item_id}
        stock_find = stock.add_resource("find").add_resource("{item_id}")
        stock_find.add_method("GET", stock_find_integration)

        # POST /stock/add/{item_id}/{number}
        stock_add = stock.add_resource("add").add_resource("{item_id}").add_resource("{number}")
        stock_add.add_method("POST", stock_add_integration)

        # POST /stock/subtract/{item_id}/{number}
        stock_subtract = stock.add_resource("subtract").add_resource("{item_id}").add_resource("{number}")
        stock_subtract.add_method("POST", stock_subtract_integration)

        # PAYMENT RESOURCE
        payment = api.root.add_resource("payment")

        # GET /payment/status/{order_id}
        payment_status = payment.add_resource("status").add_resource("{order_id}")
        payment_status.add_method("GET", payment_status_integration)

        # POST /payment/pay/{order_id}/{amount}
        payment_pay = payment.add_resource("pay").add_resource("{order_id}").add_resource("{amount}")
        payment_pay.add_method("POST", payment_pay_integration)

        # POST /payment/cancel/{order_id}
        payment_cancel = payment.add_resource("cancel").add_resource("{order_id}")
        payment_cancel.add_method("POST", payment_cancel_integration)
        
        # Permissions
        users_table.grant_read_write_data(users_create_lambda)
        users_table.grant_read_write_data(users_find_lambda)
        users_table.grant_read_write_data(users_remove_lambda)
        users_table.grant_read_write_data(users_credit_subtract_lambda)
        users_table.grant_read_write_data(users_credit_add_lambda)
        users_table.grant_read_write_data(payment_pay_lambda)
        users_table.grant_read_write_data(payment_cancel_lambda)

        orders_table.grant_read_write_data(orders_create_lambda)
        orders_table.grant_read_write_data(orders_remove_lambda)
        orders_table.grant_read_write_data(orders_find_lambda)
        orders_table.grant_read_write_data(orders_item_add_lambda)
        orders_table.grant_read_write_data(orders_item_remove_lambda)
        orders_table.grant_read_write_data(payment_status_lambda)
        orders_table.grant_read_write_data(payment_pay_lambda)
        orders_table.grant_read_write_data(payment_cancel_lambda)

        stock_table.grant_read_write_data(stock_create_lambda)
        stock_table.grant_read_write_data(stock_find_lambda)
        stock_table.grant_read_write_data(stock_add_lambda)
        stock_table.grant_read_write_data(stock_subtract_lambda)
        stock_table.grant_read_write_data(orders_item_add_lambda)
        stock_table.grant_read_write_data(orders_item_remove_lambda)

        # Environment variables
        users_create_lambda.add_environment("USERS_TABLE", users_table.table_name)
        users_remove_lambda.add_environment("USERS_TABLE", users_table.table_name)
        users_find_lambda.add_environment("USERS_TABLE", users_table.table_name)
        users_credit_subtract_lambda.add_environment("USERS_TABLE", users_table.table_name)
        users_credit_add_lambda.add_environment("USERS_TABLE", users_table.table_name)

        orders_create_lambda.add_environment("ORDERS_TABLE", orders_table.table_name)
        orders_remove_lambda.add_environment("ORDERS_TABLE", orders_table.table_name)
        orders_find_lambda.add_environment("ORDERS_TABLE", orders_table.table_name)
        orders_item_add_lambda.add_environment("ORDERS_TABLE", orders_table.table_name)
        orders_item_add_lambda.add_environment("STOCK_TABLE", stock_table.table_name)
        orders_item_remove_lambda.add_environment("ORDERS_TABLE", orders_table.table_name)
        orders_item_remove_lambda.add_environment("STOCK_TABLE", stock_table.table_name)

        stock_create_lambda.add_environment("STOCK_TABLE", stock_table.table_name)
        stock_find_lambda.add_environment("STOCK_TABLE", stock_table.table_name)
        stock_add_lambda.add_environment("STOCK_TABLE", stock_table.table_name)
        stock_subtract_lambda.add_environment("STOCK_TABLE", stock_table.table_name)

        payment_status_lambda.add_environment("ORDERS_TABLE", orders_table.table_name)
        payment_pay_lambda.add_environment("ORDERS_TABLE", orders_table.table_name)
        payment_pay_lambda.add_environment("USERS_TABLE", users_table.table_name)
        payment_cancel_lambda.add_environment("ORDERS_TABLE", orders_table.table_name)
        payment_cancel_lambda.add_environment("USERS_TABLE", users_table.table_name)
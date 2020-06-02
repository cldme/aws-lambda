from stock_service import StockService

from aws_cdk import core
from aws_cdk import aws_lambda
from aws_cdk import aws_dynamodb
from aws_cdk import aws_apigateway


class OrdersService(core.Construct):
    def __init__(self, scope: core.Construct, id: str, resource: aws_apigateway.Resource, stock: StockService):
        super().__init__(scope, id)

        # DynamoDB
        self.table = aws_dynamodb.Table(
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

        # Lambdas
        create_lambda = aws_lambda.Function(
            self,
            "orders_create_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/orders/create"),
            memory_size=256,
            timeout=core.Duration.seconds(10),
            function_name="orders_create_lambda"
        )
        create_lambda.add_environment("ORDERS_TABLE", self.table.table_name)
        self.table.grant_read_write_data(create_lambda)

        remove_lambda = aws_lambda.Function(
            self,
            "orders_remove_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/orders/remove"),
            memory_size=256,
            timeout=core.Duration.seconds(10),
            function_name="orders_remove_lambda"
        )
        remove_lambda.add_environment("ORDERS_TABLE", self.table.table_name)
        self.table.grant_read_write_data(remove_lambda)

        find_lambda = aws_lambda.Function(
            self,
            "orders_find_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/orders/find"),
            memory_size=256,
            timeout=core.Duration.seconds(10),
            function_name="orders_find_lambda"
        )
        find_lambda.add_environment("ORDERS_TABLE", self.table.table_name)
        self.table.grant_read_write_data(find_lambda)

        item_add_lambda = aws_lambda.Function(
            self,
            "orders_item_add_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/orders/item_add"),
            memory_size=256,
            timeout=core.Duration.seconds(10),
            function_name="orders_item_add_lambda"
        )
        item_add_lambda.add_environment("ORDERS_TABLE", self.table.table_name)
        item_add_lambda.add_environment("STOCK_TABLE", stock.table.table_name)
        self.table.grant_read_write_data(item_add_lambda)
        stock.find_lambda.grant_invoke(item_add_lambda)

        item_remove_lambda = aws_lambda.Function(
            self,
            "orders_item_remove_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/orders/item_remove"),
            memory_size=256,
            timeout=core.Duration.seconds(10),
            function_name="orders_item_remove_lambda"
        )
        item_remove_lambda.add_environment("ORDERS_TABLE", self.table.table_name)
        item_remove_lambda.add_environment("STOCK_TABLE", stock.table.table_name)
        self.table.grant_read_write_data(item_remove_lambda)
        stock.find_lambda.grant_invoke(item_remove_lambda)

        self.checkout_lambda = aws_lambda.Function(
            self,
            "orders_checkout_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/orders/checkout"),
            memory_size=256,
            timeout=core.Duration.seconds(60),
            function_name="orders_checkout_lambda"
        )
        self.checkout_lambda.add_environment("ORDERS_TABLE", self.table.table_name)
        self.table.grant_read_write_data(self.checkout_lambda)
        stock.add_lambda.grant_invoke(self.checkout_lambda)
        stock.subtract_lambda.grant_invoke(self.checkout_lambda)

        # API Gateway Lambda integrations
        create_integration = aws_apigateway.LambdaIntegration(create_lambda)
        remove_integration = aws_apigateway.LambdaIntegration(remove_lambda)
        find_integration = aws_apigateway.LambdaIntegration(find_lambda)
        item_add_integration = aws_apigateway.LambdaIntegration(item_add_lambda)
        item_remove_integration = aws_apigateway.LambdaIntegration(item_remove_lambda)
        checkout_integration = aws_apigateway.LambdaIntegration(self.checkout_lambda)

        # API Gateway
        # POST /orders/create/{user_id}
        create = resource.add_resource("create").add_resource("{user_id}")
        create.add_method("POST", create_integration)

        # DELETE /orders/remove/{order_id}
        remove = resource.add_resource("remove").add_resource("{order_id}")
        remove.add_method("DELETE", remove_integration)

        # GET /orders/find/{order_id}
        find = resource.add_resource("find").add_resource("{order_id}")
        find.add_method("GET", find_integration)

        # POST /orders/addItem/{order_id}/{item_id}
        item_add = resource.add_resource("addItem").add_resource("{order_id}").add_resource("{item_id}")
        item_add.add_method("POST", item_add_integration)

        # DELETE /orders/removeItem/{order_id}/{item_id}
        item_remove = resource.add_resource("removeItem").add_resource("{order_id}").add_resource("{item_id}")
        item_remove.add_method("DELETE", item_remove_integration)

        # POST /orders/checkout/{order_id}
        checkout = resource.add_resource("checkout").add_resource("{order_id}")
        checkout.add_method("POST", checkout_integration)

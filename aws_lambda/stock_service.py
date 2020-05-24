from aws_cdk import core
from aws_cdk import aws_lambda
from aws_cdk import aws_dynamodb
from aws_cdk import aws_apigateway


class StockService(core.Construct):
    def __init__(self, scope: core.Construct, id: str, resource: aws_apigateway.Resource):
        super().__init__(scope, id)

        # DynamoDB
        self.table = aws_dynamodb.Table(
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
        create_lambda = aws_lambda.Function(
            self,
            "stock_create_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/stock/create"),
            function_name="stock_create_lambda"
        )
        create_lambda.add_environment("STOCK_TABLE", self.table.table_name)
        self.table.grant_read_write_data(create_lambda)

        find_lambda = aws_lambda.Function(
            self,
            "stock_find_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/stock/find"),
            function_name="stock_find_lambda"
        )
        find_lambda.add_environment("STOCK_TABLE", self.table.table_name)
        self.table.grant_read_write_data(find_lambda)

        add_lambda = aws_lambda.Function(
            self,
            "stock_add_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/stock/add"),
            function_name="stock_add_lambda"
        )
        add_lambda.add_environment("STOCK_TABLE", self.table.table_name)
        self.table.grant_read_write_data(add_lambda)

        subtract_lambda = aws_lambda.Function(
            self,
            "stock_subtract_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/stock/subtract"),
            function_name="stock_subtract_lambda"
        )
        subtract_lambda.add_environment("STOCK_TABLE", self.table.table_name)
        self.table.grant_read_write_data(subtract_lambda)

        # API Gateway integration
        create_integration = aws_apigateway.LambdaIntegration(create_lambda)
        find_integration = aws_apigateway.LambdaIntegration(find_lambda)
        add_integration = aws_apigateway.LambdaIntegration(add_lambda)
        subtract_integration = aws_apigateway.LambdaIntegration(subtract_lambda)

        # API Gateway
        # POST /stock/item/create/{price}
        create = resource.add_resource("item").add_resource("create").add_resource("{price}")
        create.add_method("POST", create_integration)

        # GET /stock/find/{item_id}
        find = resource.add_resource("find").add_resource("{item_id}")
        find.add_method("GET", find_integration)

        # POST /stock/add/{item_id}/{number}
        add = resource.add_resource("add").add_resource("{item_id}").add_resource("{number}")
        add.add_method("POST", add_integration)

        # POST /stock/subtract/{item_id}/{number}
        subtract = resource.add_resource("subtract").add_resource("{item_id}").add_resource("{number}")
        subtract.add_method("POST", subtract_integration)
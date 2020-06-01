from aws_cdk import aws_apigateway
from aws_cdk import aws_dynamodb
from aws_cdk import aws_lambda
from aws_cdk import core


class UsersService(core.Construct):
    def __init__(self, scope: core.Construct, id: str, resource: aws_apigateway.Resource):
        super().__init__(scope, id)

        # DynamoDB
        self.table = aws_dynamodb.Table(
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

        # Lambdas
        create_lambda = aws_lambda.Function(
            self,
            "users_create_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/users/create"),
            memory_size=256,
            timeout=core.Duration.seconds(10),
            function_name="users_create_lambda"
        )
        create_lambda.add_environment("USERS_TABLE", self.table.table_name)
        self.table.grant_read_write_data(create_lambda)

        find_lambda = aws_lambda.Function(
            self,
            "users_find_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/users/find"),
            memory_size=256,
            timeout=core.Duration.seconds(10),
            function_name="users_find_lambda"
        )
        find_lambda.add_environment("USERS_TABLE", self.table.table_name)
        self.table.grant_read_write_data(find_lambda)

        remove_lambda = aws_lambda.Function(
            self,
            "users_remove_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/users/remove"),
            memory_size=256,
            timeout=core.Duration.seconds(10),
            function_name="users_remove_lambda"
        )
        remove_lambda.add_environment("USERS_TABLE", self.table.table_name)
        self.table.grant_read_write_data(remove_lambda)

        credit_subtract_lambda = aws_lambda.Function(
            self,
            "users_credit_subtract_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/users/credit_subtract"),
            memory_size=256,
            timeout=core.Duration.seconds(10),
            function_name="users_credit_subtract_lambda"
        )
        credit_subtract_lambda.add_environment("USERS_TABLE", self.table.table_name)
        self.table.grant_read_write_data(credit_subtract_lambda)

        credit_add_lambda = aws_lambda.Function(
            self,
            "users_credit_add_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/users/credit_add"),
            memory_size=256,
            timeout=core.Duration.seconds(10),
            function_name="users_credit_add_lambda"
        )
        credit_add_lambda.add_environment("USERS_TABLE", self.table.table_name)
        self.table.grant_read_write_data(credit_add_lambda)

        # API Gateway Lambda integrations
        create_integration = aws_apigateway.LambdaIntegration(create_lambda)
        find_integration = aws_apigateway.LambdaIntegration(find_lambda)
        remove_integration = aws_apigateway.LambdaIntegration(remove_lambda)
        credit_subtract_integration = aws_apigateway.LambdaIntegration(credit_subtract_lambda)
        credit_add_integration = aws_apigateway.LambdaIntegration(credit_add_lambda)

        # API Gateway
        credit = resource.add_resource("credit")

        # POST /users/create
        create = resource.add_resource("create")
        create.add_method("POST", create_integration)

        # DELETE /users/remove/{user_id}
        remove = resource.add_resource("remove").add_resource("{user_id}")
        remove.add_method("DELETE", remove_integration)

        # GET /users/find/{user_id}
        find = resource.add_resource("find").add_resource("{user_id}")
        find.add_method("GET", find_integration)

        # POST /users/credit/subtract/{user_id}/{amount}
        credit_subtract = credit.add_resource("subtract").add_resource("{user_id}").add_resource("{amount}")
        credit_subtract.add_method("POST", credit_subtract_integration)

        # POST /users/credit/add/{user_id}/{amount}
        credit_add = credit.add_resource("add").add_resource("{user_id}").add_resource("{amount}")
        credit_add.add_method("POST", credit_add_integration)
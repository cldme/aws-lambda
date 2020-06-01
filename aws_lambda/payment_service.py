from aws_cdk import aws_apigateway
from aws_cdk import aws_lambda
from aws_cdk import core

from .orders_service import OrdersService
from .users_service import UsersService


class PaymentService(core.Construct):
    def __init__(self, scope: core.Construct, id: str, resource: aws_apigateway.Resource, users: UsersService,
                 orders: OrdersService):
        super().__init__(scope, id)

        # Lambda
        status_lambda = aws_lambda.Function(
            self,
            "payment_status_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/payment/status"),
            memory_size=256,
            timeout=core.Duration.seconds(10),
            function_name="payment_status_lambda"
        )
        status_lambda.add_environment("ORDERS_TABLE", orders.table.table_name)
        orders.table.grant_read_write_data(status_lambda)

        pay_lambda = aws_lambda.Function(
            self,
            "payment_pay_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/payment/pay"),
            memory_size=256,
            timeout=core.Duration.seconds(60),
            function_name="payment_pay_lambda"
        )
        pay_lambda.add_environment("ORDERS_TABLE", orders.table.table_name)
        pay_lambda.add_environment("USERS_TABLE", users.table.table_name)
        orders.table.grant_read_write_data(pay_lambda)
        users.table.grant_read_write_data(pay_lambda)
        pay_lambda.grant_invoke(orders.checkout_lambda)

        cancel_lambda = aws_lambda.Function(
            self,
            "payment_cancel_lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./services/payment/cancel"),
            memory_size=256,
            timeout=core.Duration.seconds(60),
            function_name="payment_cancel_lambda"
        )
        cancel_lambda.add_environment("ORDERS_TABLE", orders.table.table_name)
        cancel_lambda.add_environment("USERS_TABLE", users.table.table_name)
        orders.table.grant_read_write_data(cancel_lambda)
        users.table.grant_read_write_data(cancel_lambda)
        cancel_lambda.grant_invoke(orders.checkout_lambda)

        # API Gateway integration
        status_integration = aws_apigateway.LambdaIntegration(status_lambda)
        pay_integration = aws_apigateway.LambdaIntegration(pay_lambda)
        cancel_integration = aws_apigateway.LambdaIntegration(cancel_lambda)

        # API Gateway
        # GET /payment/status/{order_id}
        status = resource.add_resource("status").add_resource("{order_id}")
        status.add_method("GET", status_integration)

        # POST /payment/pay/{order_id}/{amount}
        pay = resource.add_resource("pay").add_resource("{order_id}").add_resource("{amount}")
        pay.add_method("POST", pay_integration)

        # POST /payment/cancel/{order_id}
        cancel = resource.add_resource("cancel").add_resource("{order_id}")
        cancel.add_method("POST", cancel_integration)

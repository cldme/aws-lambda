from aws_cdk import aws_apigateway
from aws_cdk import core
from orders_service import OrdersService
from payment_service import PaymentService
from stock_service import StockService
from users_service import UsersService


class AwsLambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # REST API
        api = aws_apigateway.RestApi(self, "webshop-api", rest_api_name="webshop-api")

        # USERS RESOURCE
        users_resource = api.root.add_resource("users")
        users = UsersService(self, "users", users_resource)

        # STOCK RESOURCE
        stock_resource = api.root.add_resource("stock")
        stock = StockService(self, "stock", stock_resource)

        # ORDERS RESOURCE
        orders_resource = api.root.add_resource("orders")
        orders = OrdersService(self, "orders", orders_resource, stock)

        # PAYMENT RESOURCE
        payment_resource = api.root.add_resource("payment")
        payment = PaymentService(self, "payments", payment_resource, users, orders)





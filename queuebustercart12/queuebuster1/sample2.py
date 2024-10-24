from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.customer_details import CustomerDetails
from cashfree_pg.models.order_meta import OrderMeta

Cashfree.XClientId = "TEST103249226ce0eb2c37ee62680bc722942301"
Cashfree.XClientSecret = "cfsk_ma_test_e0c093c7529b1bb8ac0faf448326ff2b_6396be77"
Cashfree.XEnvironment = Cashfree.SANDBOX
x_api_version = "2023-08-01"

customerDetails = CustomerDetails(customer_id="devstudio_user", customer_phone="8474090589")

createOrderRequest = CreateOrderRequest(order_id="devstudio_10897193", order_amount=1.00, order_currency="INR", customer_details=customerDetails)

orderMeta = OrderMeta()
orderMeta.return_url = "https://www.cashfree.com/devstudio/preview/pg/web/checkout?order_id={order_id}";
createOrderRequest.order_meta = orderMeta;

try:
    api_response = Cashfree().PGCreateOrder(x_api_version, createOrderRequest, None, None)
    print(api_response.data)
except Exception as e:
    print(e)
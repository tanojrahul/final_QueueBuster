# # import requests
# # import json
# #
# # # Cashfree API credentials (Replace these with your API keys)
# # API_KEY = 'TEST103249226ce0eb2c37ee62680bc722942301'
# # SECRET_KEY = 'cfsk_ma_test_e0c093c7529b1bb8ac0faf448326ff2b_6396be77'
# #
# # BASE_URL = 'https://sandbox.cashfree.com/pg/orders'  # Sandbox URL
# # # BASE_URL='https://api.cashfree.com/pg/orders'
# # # Order data to be sent
# # order_payload = {
# #     "customer_details": {
# #         "customer_id": "12345",
# #         "customer_email": "customer@example.com",
# #         "customer_phone": "9999999999"
# #     },
# #     "order_id": "order_004",  # Unique order ID
# #     "order_amount": 500.00,  # Amount in INR
# #     "order_currency": "INR",
# #     "order_note": "Payment for XYZ product",
# #     "order_meta": {
# #         "return_url": "https://yourwebsite.com/payment-status?order_id={order_id}",
# #         "notify_url": "https://yourwebsite.com/webhook"
# #     }
# # }
# #
# # # Headers with API version and authentication
# # headers = {
# #     "Accept": "application/json",
# #     "Content-Type": "application/json",
# #     "x-api-version": "2022-09-01",  # Valid API version
# #     "x-client-id": API_KEY,
# #     "x-client-secret": SECRET_KEY
# # }
# #
# # # Send POST request to create an order
# # response = requests.post(BASE_URL, data=json.dumps(order_payload), headers=headers)
# #
# # # Check the response and extract the payment URL
# # if response.status_code == 200:
# #     response_data = response.json()
# #     payment_url = response_data.get("payments", {}).get("url")  # Extract payment link
# #     if payment_url:
# #         print("Payment Link:", payment_url)
# #     else:
# #         print("No payment link found in response:", response_data)
# # else:
# #     print(f"Error: {response.status_code} - {response.text}")
#
#
#
# ''''''
# from cashfree_pg.models.create_order_request import CreateOrderRequest
# from cashfree_pg.api_client import Cashfree
# from cashfree_pg.models.customer_details import CustomerDetails
# from cashfree_pg.models.order_meta import OrderMeta
#
# Cashfree.XClientId = "TEST103249226ce0eb2c37ee62680bc722942301"
# Cashfree.XClientSecret = "cfsk_ma_test_e0c093c7529b1bb8ac0faf448326ff2b_6396be77"
# Cashfree.XEnvironment = Cashfree.SANDBOX
# x_api_version = "2023-08-01"
#
#
# customerDetails = CustomerDetails(customer_id="walterwNrcMi", customer_phone="9999999999")
# orderMeta = OrderMeta(return_url="https://www.cashfree.com/devstudio/preview/pg/web/checkout?order_id={order_id}")
# createOrderRequest = CreateOrderRequest(order_amount=1, order_currency="INR", customer_details=customerDetails, order_meta=orderMeta)
# try:
#     api_response = Cashfree().PGCreateOrder(x_api_version, createOrderRequest, None, None)
#     print(api_response.data)
# except Exception as e:
#     print(e)
#
#
# try:
#     api_response = Cashfree().PGOrderFetchPayments(x_api_version, "order_103249222nqn9FpVJz6rf2PqYSuOogSL6Mt", None)
#     print(api_response.data)
# except Exception as e:
#     print(e)


import cashfree_sdk

# Listing contents of the cashfree_sdk package
# print(cashfree_sdk.__path__)  # This gives you the path to the package
#
# # Assuming you have a configuration for Cashfree setup
# import Cashfree
#
# def setup_cashfree():
#     app_id = "TEST103249226ce0eb2c37ee62680bc722942301"
#     secret_key = "cfsk_ma_test_e0c093c7529b1bb8ac0faf448326ff2b_6396be77"
#     Cashfree().set_credentials(app_id=app_id, secret_key=secret_key)
#
# import os
#
# # Path to the cashfree_sdk package
# path = r"C:\Users\avula\PycharmProjects\pythonProject\.venv\Lib\site-packages\cashfree_sdk"
# print(os.listdir(path))
#


from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.customer_details import CustomerDetails
from cashfree_pg.models.order_meta import OrderMeta
from cashfree_pg.api_client import Cashfree
Cashfree.XClientId = "775915c89f863292533318c921519577"
Cashfree.XClientSecret = "cfsk_ma_prod_a118c35ba2dcebae44ea512153524292_800d4fde"
Cashfree.XEnvironment = Cashfree.SANDBOX
x_api_version = "2023-08-01"
#
# customer_details = CustomerDetails(customer_id="123", customer_phone="9999999999")
#
# # Create order request
# create_order_request = CreateOrderRequest(order_amount=float(25000), order_currency="INR",
#                                           customer_details=customer_details)
# order_meta = OrderMeta(return_url="http://localhost:8000/successful")  # Adjust return URL
# create_order_request.order_meta = order_meta
#
# # Call the Cashfree API to create the order
# try:
#     api_response = Cashfree().PGCreateOrder(x_api_version, create_order_request, None, None)
#     payment_session_id = api_response.data.payment_session_id  # Correct way to access the attribute
#     print({'status': 'success', 'payment_session_id': payment_session_id})
# except Exception as e:
#     print(f"Error creating order: {str(e)}")
#     print({'status': 'error', 'message': f'Error creating order: {str(e)}'})

customerDetails = CustomerDetails(customer_id="walterwNrcMi", customer_phone="9999999999")
orderMeta = OrderMeta(return_url="https://www.cashfree.com/devstudio/preview/pg/web/checkout?order_id={order_id}")
createOrderRequest = CreateOrderRequest(order_amount=1, order_currency="INR", customer_details=customerDetails, order_meta=orderMeta)
try:
    api_response = Cashfree().PGCreateOrder(x_api_version, createOrderRequest, None, None)
    print(api_response.data)
except Exception as e:
    print(e)


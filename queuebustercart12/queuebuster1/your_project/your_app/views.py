from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import CartItem, Product, Cart  # Ensure Cart is imported

from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.customer_details import CustomerDetails
from cashfree_pg.models.order_meta import OrderMeta


Cashfree.XClientId = "775915c89f863292533318c921519577"
Cashfree.XClientSecret = "cfsk_ma_prod_a118c35ba2dcebae44ea512153524292_800d4fde"
Cashfree.XEnvironment = Cashfree.SANDBOX
x_api_version = "2023-08-01"


ADMIN_USERNAMES = ['admin1', 'admin2']  # Add your admin usernames here


from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.customer_details import CustomerDetails

#
# def create_order():
#         customerDetails = CustomerDetails(customer_id="123", customer_phone="9999999999")
#         createOrderRequest = CreateOrderRequest(order_amount=1, order_currency="INR", customer_details=customerDetails)
#         try:
#             api_response = Cashfree().PGCreateOrder(x_api_version, createOrderRequest, None, None)
#             print(api_response.data)
#         except Exception as e:
#             print(e)

# views.py
from django.shortcuts import render, redirect
from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.customer_details import CustomerDetails
from cashfree_pg.models.order_meta import OrderMeta
from .models import Product

Cashfree.XClientId = "TEST103249226ce0eb2c37ee62680bc722942301"
Cashfree.XClientSecret = "cfsk_ma_test_e0c093c7529b1bb8ac0faf448326ff2b_6396be77"
Cashfree.XEnvironment = Cashfree.SANDBOX
x_api_version = "2023-08-01"
import uuid  # Importing uuid to generate unique order IDs

import random
import string

def generate_order_id(length=8):
    return "devstudio_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# Generate a random order ID
order_id = generate_order_id()


def checkout(request):
    cart = get_or_create_cart(request.user)
    # products = Product.objects.filter(barcode__in=cart)
    cart_items = CartItem.objects.filter(cart=cart)

    # total_amount = sum([product.price for product in products])+1
    subtotal = sum(item.subtotal() for item in cart_items)

    customer_details = CustomerDetails(
        customer_id="devstudio_user", customer_phone="8474090589"
    )

    # Generate a random unique order ID
    order_id = f"devstudio_{uuid.uuid4().hex}"

    create_order_request = CreateOrderRequest(
        order_id=order_id,
        order_amount=float(subtotal),
        order_currency="INR",
        customer_details=customer_details,
    )

    order_meta = OrderMeta(
        return_url="https://www.cashfree.com/devstudio/preview/pg/web/checkout?order_id={order_id}"
    )
    create_order_request.order_meta = order_meta

    try:
        api_response = Cashfree().PGCreateOrder(
            x_api_version, create_order_request, None, None
        )
        payment_session_id = api_response.data.payment_session_id
    except Exception as e:
        return render(request, "error.html", {"message": str(e)})

    return render(request, "checkout.html", {"payment_session_id": payment_session_id})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
 # Ensure this is the correct import based on your SDK
from decimal import Decimal

@csrf_exempt
@login_required  # Ensure the user is logged in
def create_order(request):
    if request.method == 'POST':
        # Get or create the user's cart
        cart = get_or_create_cart(request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            return JsonResponse({'status': 'error', 'message': 'Your cart is empty!'})

        total_amount = Decimal('0.00')  # Initialize total_amount as Decimal
        # Calculate the total amount from the cart
        for item in cart_items:
            # Convert item.product.price to float or keep using Decimal for consistency
            total_amount += item.product.price * item.quantity  # This will now work correctly with Decimal

        print(f"Total amount calculated: {total_amount}")

        # Ensure the total amount is greater than or equal to 1
        if total_amount < Decimal('1.00'):
            return JsonResponse({'status': 'error', 'message': 'Total amount must be at least 1'})

        # Create customer details (adjust as necessary)
        customer_details = CustomerDetails(customer_id="123", customer_phone="9999999999")  # Update with actual customer data
        print(total_amount)
        # Create order request
        create_order_request = CreateOrderRequest(order_amount=float(total_amount), order_currency="INR",
                                                  customer_details=customer_details)
        order_meta = OrderMeta(return_url="http://localhost:8000/successful")  # Adjust return URL
        create_order_request.order_meta = order_meta

        # Call the Cashfree API to create the order
        try:
            api_response = Cashfree().PGCreateOrder(x_api_version, create_order_request, None, None)
            payment_session_id = api_response.data.payment_session_id  # Correct way to access the attribute
            return JsonResponse({'status': 'success', 'payment_session_id': payment_session_id})
        except Exception as e:
            print(f"Error creating order: {str(e)}")
            return JsonResponse({'status': 'error', 'message': f'Error creating order: {str(e)}'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



def payment_success(request):
    return render(request, 'payment-success.html')

# Function to check if the user is an admin
def is_admin(user):
    return user.username in ADMIN_USERNAMES


# Utility function to get or create a cart for a user
def get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


# Login view (redirect based on user type)
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')

            if is_admin(user):  # Redirect admin users to the admin dashboard
                return redirect('admin_dashboard')
            else:
                return redirect('home')  # Redirect regular users to the main home page
        else:
            messages.error(request, 'Invalid username or password!')

    return render(request, 'login.html')


@login_required
def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')


@login_required
def scan_product_view(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        try:
            product = Product.objects.get(barcode=product_id)
            return JsonResponse({'success': True, 'message': 'Product found: ' + product.name})
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found in database.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


# Register view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please try again.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Create or update the cart item
    cart = get_or_create_cart(request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')


@login_required
def cart_view(request):
    cart = get_or_create_cart(request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return HttpResponse("Your cart is empty!")

    subtotal = sum(item.subtotal() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'subtotal': subtotal})


@login_required
def scan_view(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        try:
            product = Product.objects.get(barcode=product_id)  # Assuming barcode is used
            cart = get_or_create_cart(request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            if not created:
                cart_item.quantity += 1
            cart_item.save()

            return JsonResponse({'success': True, 'message': 'Product added to cart.'})
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found.'}, status=404)

    return render(request, 'scan.html')


def home_view(request):
    return render(request, 'home.html')


# Admin views
@login_required
def product_management(request):
    products = Product.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        # You may add fields like description, quantity etc. as needed
        product = Product.objects.create(name=name, price=price)
        messages.success(request, f'Product "{product.name}" added successfully!')
        return redirect('product_management')

    return render(request, 'admin/product_management.html', {'products': products})


@login_required
def checkout_view(request):
    # Implement your checkout logic here
    cart = get_or_create_cart(request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return HttpResponse("Your cart is empty!")

    subtotal = sum(item.subtotal() for item in cart_items)
    return render(request, 'checkout.html',{'subtotal': subtotal})


@login_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'admin/manage_users.html', {'users': users})


@login_required
def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        cart_item.delete()  # Remove the item from the cart
        messages.success(request, 'Item removed from cart successfully!')
    except CartItem.DoesNotExist:
        messages.error(request, 'Item not found in cart.')

    return redirect('cart')


@login_required
def manage_products(request):
    products = Product.objects.all()
    return render(request, 'admin/manage_products.html', {'products': products})


@login_required
def remove_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, f'Product "{product.name}" removed successfully!')
    return redirect('manage_products')


@login_required
def add_product_scan(request):
    if request.method == 'POST':
        # Handle the scanned barcode and add product logic here
        pass
    return render(request, 'admin/add_product_scan.html')


@login_required
def user_management(request):
    users = User.objects.all()
    return render(request, 'admin/user_management.html', {'users': users})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout


@login_required
def admin_scan_view(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        return redirect('admin_add_product', product_id=product_id)

    return render(request, 'admin/admin_scan.html')


def add_product_view(request, barcode):
    barcode = barcode.strip()  # Clean up any spaces around the barcode

    # Check if the product with the barcode exists
    try:
        product = Product.objects.get(barcode=barcode)
        product_exists = True
    except Product.DoesNotExist:
        product = None
        product_exists = False

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')

        # Create a new product if it doesn't exist, otherwise update the existing one
        if not product_exists:
            product = Product.objects.create(
                barcode=barcode,
                name=product_name,
                description=description,
                price=price,
                quantity=quantity,
            )
            messages.success(request, 'New product added successfully!')
        else:
            product.name = product_name
            product.description = description
            product.price = price
            product.quantity = quantity
            product.save()
            messages.success(request, 'Product updated successfully!')

        return redirect('admin_scan')  # Redirect to admin scan after adding/updating

    return render(request, 'admin/admin_add_product.html', {
        'barcode': barcode,
        'product': product,
        'product_exists': product_exists,
    })


def contact_view(request):
    return render(request, 'contact.html')  # Make sure you have a 'contact.html' template


def terms_conditions_view(request):
    return render(request, 'terms_conditions.html')  # Make sure you have a 'terms_conditions.html' template
import requests
import time
from django.conf import settings
from django.shortcuts import render, redirect



def payment_success(request):
    return render(request, 'payment-success.html')

from django.conf import settings
import requests
from django.conf import settings
import requests
from django.shortcuts import redirect, HttpResponse

def payment(request):
    total_amount = request.session.get('cart_total')  # Example: Retrieve total from session
    order_id = "ORDER123"  # Generate this dynamically

    # Customer details
    customer_details = {
        "customer_id": "123",
        "customer_email": "test@example.com",
        "customer_phone": "9999999999"
    }


    # Data to send in the request
    data = {
        "order_id": order_id,
        "order_amount": total_amount,
        "order_currency": "INR",
        "customer_details": customer_details,
        "return_url": settings.CASHFREE_RETURN_URL,
    }

    headers = {
        "x-client-id": settings.CASHFREE_CLIENT_ID,
        "x-client-secret": settings.CASHFREE_CLIENT_SECRET,
        "x-api-version": "2022-09-01",
        "Content-Type": "application/json",
    }

    try:
        # Send the request to create an order
        response = requests.post(
            settings.CASHFREE_PAYMENT_URL, headers=headers, json=data
        )
        response_data = response.json()

        if response.status_code == 200:
            # Redirect user to Cashfree payment link
            payment_link = response_data['payment_link']
            return redirect(payment_link)
        else:
            # Display error message from Cashfree
            return HttpResponse(f"Error: {response_data.get('message', 'Payment failed')}")

    except Exception as e:
        # Handle any exception that occurs
        return HttpResponse(f"An error occurred: {str(e)}")

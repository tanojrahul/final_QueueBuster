from django.urls import path
from . import views
from django.contrib import admin
from .views import remove_from_cart, checkout_view  # Import views

urlpatterns = [
    path('login/', views.login_view, name='login'),  # User login
    path('register/', views.register_view, name='register'),  # User registration
    path('scan/', views.scan_view, name='scan'),  # Scan products
    path('cart/', views.cart_view, name='cart'),  # View the cart
    path('', views.home_view, name='home'),  # Home page
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Add product to cart
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard
    path('admin1/manage_users/', views.manage_users, name='manage_users'),  # Manage users
    path('admin1/scan/', views.admin_scan_view, name='admin_scan'),  # Admin scan
    path('admin1/manage_products/', views.manage_products, name='manage_products'),  # Manage products
    path('admin1/add_product_scan/', views.add_product_scan, name='add_product_scan'),  # Add product by scan
    path('logout/', views.logout_view, name='logout'),  # Logout user
    path('admin1/add-product/<str:barcode>/', views.add_product_view, name='add_product'),  # Add product with barcode
    path('remove_from_cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),  # Remove item from cart
    path('checkout1/', checkout_view, name='checkout'),  # Checkout view
    path('admin1/remove-product/<int:product_id>/', views.remove_product, name='remove_product'),  # Remove product
    path('contact/', views.contact_view, name='contact'),  # Contact page
    path('terms/', views.terms_conditions_view, name='terms_conditions'),  # Terms and conditions page
    path('checkout2/', views.checkout, name='checkout'),
    path('payment/', views.create_order, name='payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('create-order/', views.create_order, name='create_order'),
]


from django.urls import path

from . import views
from .views import basic_api_response, view_stores

app_name = "shop"

urlpatterns = [
    # Home page
    path(
        '',
        views.welcome,
        name='home'
    ),

    # Login
    path(
        'login/',
        views.login_user,
        name='login'
    ),

    # Logout
    path(
        'logout/',
        views.logout_user,
        name='logout'
    ),

    # API
    path(
        "api/stores/",
        views.basic_api_response,
        name="basic_api_response"
    ),

    # Registration
    path(
        'register/',
        views.register_user,
        name='register'
    ),

    # Welcome
    path(
        'welcome/',
        views.welcome,
        name='welcome'
    ),
    
    # Basic API Response
    path(
        'basic_response/', basic_api_response
    ),
    
    # View Stores
    path(
        'get/stores', view_stores
    ),

    # Stores
    path(
        'stores/',
        views.store_list,
        name='store_list'
    ),

    # Create Store
    path(
        'stores/create/',
        views.create_store,
        name='create_store'
    ),

    # Edit Store
    path(
        'stores/<int:store_id>/edit/',
        views.edit_store,
        name='edit_store'
    ),

    # Delete Store
    path(
        'stores/<int:store_id>/delete/',
        views.delete_store,
        name='delete_store'
    ),

    # Products
    path(
        'products/',
        views.product_list,
        name='product_list'
    ),

    # Vendor Products
    path(
        'products/vendor/',
        views.vendor_products,
        name='vendor_products'
    ),

    # Add Product
    path(
        'products/add/',
        views.add_product,
        name='add_product'
    ),

    # Edit Product
    path(
        'products/<int:product_id>/edit/',
        views.edit_product,
        name='edit_product'
    ),

    # Delete Product
    path(
        'products/<int:product_id>/delete/',
        views.delete_product,
        name='delete_product'
    ),

    # Cart
    path(
        'cart/',
        views.show_user_cart,
        name='cart_page'
    ),

    # Add item to cart
    path(
        'cart/add/',
        views.add_item_to_cart,
        name='add_item_to_cart'
    ),

    # Checkout
    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),

    # Reviews
    path(
        'products/<int:product_id>/review/',
        views.add_review,
        name='add_review'
    ),

    # Password reset
    path(
        'reset_password/<str:token>/',
        views.reset_user_password,
        name='password_reset'
    ),

    # Reset password request
    path(
        'reset_password/',
        views.reset_password,
        name='reset_password'
    ),

    # Password reset request confirmation
    path(
        'request_password_reset/',
        views.request_password_reset,
        name='request_password_reset'
    ),

    # Reddit feed
    path(
        "reddit/",
        views.reddit_feed,
        name="reddit_feed"
    ),

    # Add Store API
    path(
        'api/stores/add/',
        views.add_store,
        name='add_store'
        ),

    # Add Product API
    path(
        'api/products/add/',
        views.add_product_api,
        name='add_product_api'
        ),

    # Add Review API
    path(
        'api/reviews/',
        views.get_reviews_api,
        name='get_reviews_api'
        ),

    # Get Vendor Stores API
    path(
        'api/vendors/<int:vendor_id>/stores/',
        views.get_vendor_stores,
        name='get_vendor_stores'
    ),

    # Get Store Products API
    path(
        'api/stores/<int:store_id>/products/',
        views.get_store_products,
        name='get_store_products'
    ),

]

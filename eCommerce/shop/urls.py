from django.urls import path

from . import views

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
]

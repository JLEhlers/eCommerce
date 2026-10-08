# Import necessary modules and classes
import secrets
from datetime import datetime, timedelta
from functools import wraps
from hashlib import sha1

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.http import (
    HttpResponseForbidden,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    renderer_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_xml.renderers import XMLRenderer

from .functions.reddit import get_reddit_posts
from .models import (
    Order,
    OrderItem,
    Product,
    ResetToken,
    Review,
    Store,
    UserProfile,
)
from .serializers import ProductSerializer, ReviewSerializer, StoreSerializer


# Create a function to register a new user
def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")
        email = request.POST.get("email")
        role = request.POST.get("role")

        if password != password_confirm:
            return render(
                request,
                "shop/register.html",
                {"error": "Passwords do not match."}
            )

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        UserProfile.objects.create(
            user=user,
            role=role
        )

        user.save()
        login(request, user)

        return redirect(reverse("shop:welcome"))

    return render(request, "shop/register.html")


# Create a function to log in a user
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Logout user when they close the browser
            request.session.set_expiry(0)

            return HttpResponseRedirect(reverse('shop:welcome'))
        else:
            return render(request, 'shop/login.html',
                          {'error': 'Invalid credentials'})
    return render(request, 'shop/login.html')


# Create a function to log out a user
def logout_user(request):
    if request.user is not None:
        logout(request)
        return HttpResponseRedirect(reverse('shop:login'))


# Create a function to change a user's password
def change_user_password(username, new_password):
    user = User.objects.get(username=username)
    user.set_password(new_password)
    user.save()


# Create a function to display the welcome page
@login_required
def welcome(request):
    if request.user.is_authenticated:
        return render(request, 'shop/welcome.html')
    else:
        return HttpResponseRedirect(reverse('shop:login'))


# Create a decorator to restrict access to vendors only
def vendor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if (
            request.user.is_authenticated
            and request.user.userprofile.role == "vendor"
        ):
            return view_func(request, *args, **kwargs)

        return HttpResponseForbidden(
            "Only vendors can access this page."
        )

    return wrapper


# Create a decorator to restrict access to buyers only
def buyer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if (
            request.user.is_authenticated
            and request.user.userprofile.role == "buyer"
        ):
            return view_func(request, *args, **kwargs)

        return HttpResponseForbidden(
            "Only buyers can access this page."
        )

    return wrapper


# Create a function to view all stores using the API
@api_view(['GET'])
@renderer_classes((XMLRenderer,))
def view_stores(request):
    if request.method == "GET":
        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True)

        return JsonResponse(
            data=serializer.data,
            safe=False
        )


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def add_store(request):
    vendor_id = request.data.get('vendor')

    if vendor_id is None:
        return Response(
            {'error': 'Vendor field is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if int(vendor_id) != request.user.id:
        return Response(
            {'error': 'User ID and vendor ID do not match.'},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = StoreSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


# Create a function to add a product using the API
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def add_product_api(request):

    if not hasattr(request.user, 'userprofile'):
        return Response(
            {"error": "User profile not found."},
            status=400
        )

    if request.user.userprofile.role != "vendor":
        return Response(
            {"error": "Only vendors can add products."},
            status=403
        )

    store_id = request.data.get('store')

    try:
        store = Store.objects.get(id=store_id)
    except Store.DoesNotExist:
        return Response(
            {"error": "Store not found."},
            status=404
        )

    if store.owner != request.user:
        return Response(
            {"error": "You can only add products to your own store."},
            status=403
        )

    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(store=store)
        return Response(
            serializer.data,
            status=201
        )

    return Response(serializer.errors, status=400)


# Create a function to retrieve reviews using the API
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_reviews_api(request):
    """Allow authenticated vendors to retrieve reviews."""
    
    if not hasattr(request.user, 'userprofile'):
        return Response(
            {"error": "User profile not found."},
            status=400
        )

    if request.user.userprofile.role != "vendor":
        return Response(
            {"error": "Only vendors can retrieve reviews."},
            status=403
        )

    reviews = Review.objects.all()

    serializer = ReviewSerializer(reviews, many=True)

    return Response(serializer.data)


# Create a function to retrieve stores belonging to a vendor using the API
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_vendor_stores(request, vendor_id):
    """Retrieve stores belonging to a vendor."""

    stores = Store.objects.filter(owner_id=vendor_id)

    serializer = StoreSerializer(stores, many=True)

    return Response(serializer.data)


# Create a function to retrieve products belonging to a store using the API
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_store_products(request, store_id):
    """Retrieve products belonging to a store."""

    products = Product.objects.filter(store_id=store_id)

    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)


# Create a function to fetch and display Reddit posts
def reddit_feed(request):
    # Call our helper function to fetch posts
    posts = get_reddit_posts("python")

    # Pass the posts into the template
    return render(request, "shop/reddit_feed.html", {"posts": posts})


# Create a function to display the product page
def view_product_page(request):
    user = request.user

    if user.has_perm("shop.view_product"):
        if request.method == "POST":
            product_name = request.POST.get("product")

            if not product_name:
                return render(
                    request,
                    "shop/product_page.html",
                    {"error": "No product name was given."}
                )

            try:
                product = Product.objects.get(name=product_name)

                reviews = Review.objects.filter(product=product)

                return render(
                    request,
                    "shop/product_page.html",
                    {
                        "product": product,
                        "reviews": reviews
                     }
                )

            except ObjectDoesNotExist:
                return render(
                    request,
                    "shop/product_page.html",
                    {"error": "Product not found."}
                )

        return render(request, "shop/product_page.html")

    return render(
        request,
        "shop/product_page.html",
        {"error": "You do not have permission to view this product."}
    )


# Create a function to change the price of a product
@login_required
@vendor_required
def change_product_price(request):
    user = request.user

    if user.has_perm("shop.change_product"):
        if request.method == "POST":
            product_name = request.POST.get("product")
            new_price = request.POST.get("new_price")

            if not product_name or not new_price:
                return render(request, "shop/change_price.html")

            try:
                product = Product.objects.get(name=product_name)
                product.price = float(new_price)
                product.save()

                return HttpResponseRedirect(
                    reverse("shop:products")
                )

            except ValueError:
                return render(request, "shop/change_price.html")

            except Product.DoesNotExist:
                return render(request, "shop/change_price.html")

        return render(request, "shop/change_price.html")

    return render(request, "shop/change_price.html")


# Create a function to add an item to the user's cart
@login_required
@buyer_required
def add_item_to_cart(request):
    item = request.POST.get('item')
    quantity = request.POST.get('quantity')

    if not item or not quantity:
        return redirect('cart_page')

    try:
        quantity = int(quantity)
        if quantity < 1:
            quantity = 1

    except ValueError:
        quantity = 1

    cart = request.session.get('cart', {})

    if item in cart:
        cart[item] += quantity
    else:
        cart[item] = quantity

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart_page')


# Create a function to retrieve products from the user's cart
@login_required
@buyer_required
def retrieve_products(request):
    products = []

    session = request.session

    if 'cart' in session:
        for name, quantity in session['cart'].items():
            try:
                product = Product.objects.get(name=name)

                products.append({
                    'product': product,
                    'quantity': quantity
                })

            except Product.DoesNotExist:
                pass

    return products


# Create a function to show the user's cart
@login_required
@buyer_required
def show_user_cart(request):
    cart = retrieve_products(request)

    return render(
        request,
        'shop/main_cart.html',
        {'cart': cart}
    )


# Create a function to build an email for password reset
def build_email(user, reset_url):
    subject = "Password Reset"
    user_email = user.email
    domain_email = "example@domain.com"

    body = (
        f"Hi {user.username},\n"
        f"Here is your link to reset your password: {reset_url}"
    )

    email = EmailMessage(
        subject,
        body,
        domain_email,
        [user_email]
    )

    return email


# Create a function to handle password reset requests
def request_password_reset(request):

    if request.method == "POST":

        username = request.POST.get("username")

        try:
            user = User.objects.get(username=username)

            reset_url = generate_reset_url(user)

            email = build_email(user, reset_url)
            email.send()

        except User.DoesNotExist:
            pass

        return redirect("shop:login")

    return render(
        request,
        "shop/request_password_reset.html"
    )


# Create a function to generate a reset URL for a user
def generate_reset_url(user):
    domain = "http://127.0.0.1:8000"

    url = f"{domain}/reset_password/"

    token = str(secrets.token_urlsafe(16))

    expiry_date = datetime.now() + timedelta(minutes=5)

    ResetToken.objects.create(
        user=user,
        token=sha1(token.encode()).hexdigest(),
        expiry_date=expiry_date
    )

    url += f"{token}/"

    return url


# Create a function to reset a user's password using a token
def reset_user_password(request, token):
    try:
        user_token = ResetToken.objects.get(
            token=sha1(token.encode()).hexdigest()
        )

        if user_token.expiry_date.replace(tzinfo=None) < datetime.now():
            user_token.delete()
            user_token = None
        else:
            request.session['user'] = user_token.user.username
            request.session['token'] = token

    except ResetToken.DoesNotExist:
        user_token = None

    return render(
        request,
        'shop/password_reset.html',
        {'token': user_token}
    )


# Create a function to reset a user's password
def reset_password(request):
    username = request.session['user']
    token = request.session['token']

    password = request.POST.get('password')
    password_conf = request.POST.get('password_conf')

    if password == password_conf:
        change_user_password(username, password)

        ResetToken.objects.get(
            token=sha1(token.encode()).hexdigest()
        ).delete()

        return HttpResponseRedirect(
            reverse('shop:login')
        )

    else:
        return HttpResponseRedirect(
            reverse('shop:password_reset')
        )


# Create a function to edit a store
@login_required
@vendor_required
def edit_store(request, store_id):
    store = Store.objects.get(
        id=store_id,
        owner=request.user
    )

    if request.method == "POST":
        store.name = request.POST.get("name")
        store.description = request.POST.get("description")
        store.save()

        return redirect("shop:store_list")

    return render(
        request,
        "shop/edit_store.html",
        {"store": store}
    )


# Create a function to delete a store
@login_required
@vendor_required
def delete_store(request, store_id):
    store = Store.objects.get(
        id=store_id,
        owner=request.user
    )

    store.delete()

    return redirect("shop:store_list")


# Create a function to create a store
@login_required
@vendor_required
def create_store(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")

        Store.objects.create(
            name=name,
            description=description,
            owner=request.user
        )

        return redirect("shop:store_list")

    return render(request, "shop/create_store.html")


# Create a function to display the list of stores for the logged-in user
@login_required
def store_list(request):
    stores = Store.objects.filter(
        owner=request.user
    )

    return render(
        request,
        "shop/store_list.html",
        {"stores": stores}
    )


# Create a function to add a product
@login_required
@vendor_required
def add_product(request):
    stores = Store.objects.filter(
        owner=request.user
    )

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        stock = request.POST.get("stock")
        store_id = request.POST.get("store")

        store = Store.objects.get(
            id=store_id,
            owner=request.user
        )

        Product.objects.create(
            name=name,
            description=description,
            price=price,
            stock=stock,
            store=store
        )

        return redirect("shop:vendor_products")

    return render(
        request,
        "shop/add_product.html",
        {"stores": stores}
    )


# Create a function to display the list of products owned by the logged-in user
@login_required
@vendor_required
def vendor_products(request):
    products = Product.objects.filter(
        store__owner=request.user
    )

    return render(
        request,
        "shop/vendor_products.html",
        {"products": products}
    )


# Create a function to edit a product
@login_required
@vendor_required
def edit_product(request, product_id):
    product = Product.objects.get(
        id=product_id,
        store__owner=request.user
    )

    if request.method == "POST":
        product.name = request.POST.get("name")
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")
        product.stock = request.POST.get("stock")
        product.save()

        return redirect("shop:vendor_products")

    return render(
        request,
        "shop/edit_product.html",
        {"product": product}
    )


# Create a function to delete a product
@login_required
@vendor_required
def delete_product(request, product_id):
    product = Product.objects.get(
        id=product_id,
        store__owner=request.user
    )

    product.delete()

    return redirect("shop:vendor_products")


# Create a function to display the list of products
def product_list(request):
    products = Product.objects.all()

    return render(
        request,
        "shop/product_list.html",
        {"products": products}
    )


# Create a function to add a review for a product
@login_required
@buyer_required
def add_review(request, product_id):
    if request.method == "POST":
        product = Product.objects.get(
            id=product_id
        )

        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        purchased = OrderItem.objects.filter(
            order__buyer=request.user,
            product=product
        ).exists()

        Review.objects.create(
            product=product,
            buyer=request.user,
            rating=rating,
            comment=comment,
            verified=purchased
        )

        return redirect("shop:product_list")

    return redirect("shop:product_list")


# Create a function to handle the checkout process
@login_required
@buyer_required
def checkout(request):
    cart = retrieve_products(request)

    if not cart:
        return redirect("shop:cart_page")

    total = 0

    for item in cart:
        total += item["product"].price * item["quantity"]

    if request.method == "POST":
        order = Order.objects.create(
            buyer=request.user,
            total=total
        )

        invoice = "Invoice\n\n"
        invoice += f"Order number: {order.id}\n\n"

        for item in cart:
            product = item["product"]
            quantity = item["quantity"]

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

            item_total = product.price * quantity

            invoice += (
                f"{product.name} - "
                f"{quantity} x ${product.price} = "
                f"${item_total}\n"
            )

        invoice += f"\nTotal: ${total}"

        email = EmailMessage(
            "Your Order Invoice",
            invoice,
            "example@domain.com",
            [request.user.email]
        )

        email.send()

        request.session["cart"] = {}
        request.session.modified = True

        return render(
            request,
            "shop/checkout_success.html",
            {"order": order}
        )

    return render(
        request,
        "shop/checkout.html",
        {
            "cart": cart,
            "total": total
        }
    )


# Create a function to provide a basic API response with serialized store data
def basic_api_response(request):
    if request.method == "GET":
        data = serializers.serialize(
            "json",
            Store.objects.all()
        )

        return JsonResponse(data=data, safe=False)

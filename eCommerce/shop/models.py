# Import necessary modules
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


# Create a user profile model to store additional information about users
class UserProfile(models.Model):
    """
    Model representing a user profile in the eCommerce application.

    Fields:
    - user: Links the profile to a Django user.
    - role: Stores whether the user is a buyer or vendor.

    Methods:
    - __str__: Returns a string representation of the user profile.
    """

    ROLE_CHOICES = (
        ("buyer", "Buyer"),
        ("vendor", "Vendor"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username


# Create a store model to represent stores in the application
class Store(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


# Create a product model to represent products in the application
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    stock = models.PositiveIntegerField()
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )


# Create a reset token model to handle password reset functionality
class ResetToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=500)
    expiry_date = models.DateTimeField()
    used = models.BooleanField(default=False)


# Create a review model to represent product reviews in the application
class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.buyer.username} - {self.product.name}"


# Create an order model to represent orders in the application
class Order(models.Model):
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"Order {self.id} - {self.buyer.username}"


# Create an order item model to represent items in an order
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

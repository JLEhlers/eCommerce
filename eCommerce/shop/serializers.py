from rest_framework import serializers

from .models import Product, Review, Store


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = ['owner', 'name', 'description']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'store']


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['product', 'buyer', 'rating', 'comment', 'verified']
from rest_framework import serializers
from decimal import Decimal
from store.models import Product, Collection, Review


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:  # --> model serialization
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):  # EXTERNAL RESOURCE REPRESENTATION
    class Meta:  # --> model serialization
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'inventory', 'unit_price', 'tax_price', 'collection']

    tax_price = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)  # converting float to decimal


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review

        fields = ['id', 'name', 'date', 'description', 'product_id']
        read_only_fields = ['product_id']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)

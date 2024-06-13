from rest_framework import serializers
from decimal import Decimal
from store.models import Product, Collection, Review, Cart, CartItem


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


class SimpleProduct(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProduct()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, item: CartItem):
        return item.quantity * item.product.unit_price

    """def create(self, validated_data):
        cart_id = self.context['cart_id']
        return CartItem.objects.create(cart_id=cart_id, **validated_data)"""

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    def get_total(self, cart: Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total']
        read_only_fields = ['id']

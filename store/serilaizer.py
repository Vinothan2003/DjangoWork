from rest_framework import serializers
from decimal import Decimal
from store.models import Product, Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:  # --> model serialization
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField()

    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=225)


class ProductSerializer(serializers.ModelSerializer):  # EXTERNAL RESOURCE REPRESENTATION
    class Meta:  # --> model serialization
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'inventory', 'unit_price', 'tax_price', 'collection']

    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=225)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')  # external field changed
    tax_price = serializers.SerializerMethodField(method_name='calculate_tax')

    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail'
    # )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)  # converting float to decimal

    """ 
    class ProductSerializer(serializers.Serializer):  # EXTERNAL RESOURCE REPRESENTATION
        id = serializers.IntegerField()
        title = serializers.CharField(max_length=225)
        price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')  # external field changed
        tax_price = serializers.SerializerMethodField(method_name='calculate_tax')
        collection = serializers.HyperlinkedRelatedField(
            queryset=Collection.objects.all(),
            view_name='collection-detail'
            )"""

    """def validate(self, data):
            if data['password'] != data['confirm_password']:             --> overriding the validate method
                return serializers.ValidationError("password does not match")
            return data"""

    """def create(self, validated_data):
        product = Product(**validated_data)
        product.unit_price = 1                  # --> overriding the create method
        product.save()
        return product"""

    """def update(self, instance, validated_data):     # --> overriding the update field
        instance.unit_price = validated_data.get('unit_price') 
        instance.save()
        return instance"""

    # collection = CollectionSerializer()  # --> to show in nested objects

    """
        collection = serializers.PrimaryKeyRelatedField(
            queryset=Collection.objects.all()  # --> to Show the primary key filed
    """

    # collection_name = serializers.StringRelatedField(source='collection') --> to show the string

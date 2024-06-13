from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import Response, status, APIView
from rest_framework.decorators import api_view
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination

from store.filter import ProductFilter
from store.models import Product, Collection, OrderItem, Review, Cart, CartItem
from store.serilaizer import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, \
    CartItemSerializer


# Create your views here.

# -- VIEW-SET --
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['collection_id']  # --> don't require filtering logic
    search_fields = ['title']
    ordering_fields = ['title', 'unit_price']
    # pagination_class = PageNumberPagination --> pagination

    """def get_queryset(self): # filtering logic
        queryset = Product.objects.all()
        collection_id = self.request.query_params.get('collection_id')
        if collection_id is not None:
            queryset = queryset.filter(collection_id=collection_id)
        return queryset"""

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'this method is not allowed due some reasons.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    """def deletes(self, request, id):
        product = get_object_or_404(Product, pk=id)  # getting product object
        if product.orderitems.count() > 0:  # if product have any order in the order item
            return Response({'error': 'this method is not allowed due some reasons.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)"""


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        # Collection.objects.filter(id=kwargs['pk']).first().products.all().count() > 0:
        # Collection.objects.filter(id=kwargs['pk'], products__isnull=False).exists():
        if Collection.objects.filter(id=kwargs['pk'], products__isnull=False).exists():
            return Response(
                {'error': 'collection cannot be deleted because it is the foreign key for the product table'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    # queryset = Review.objects.all() --> getting all the data
    serializer_class = ReviewSerializer

    def get_serializer_context(self):  # --> providing additional data to the serializer
        return {'product_id': self.kwargs['product_pk']}

    def get_queryset(self):  # --> getting id form th url
        return Review.objects.filter(product_id=self.kwargs['product_pk'])


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related(
        'items__product').all()  # prefetch_related('items__product') --> to get the product in db in one go
    serializer_class = CartSerializer


"""class CartItemViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    # queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer"""


class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):  # getting card id from the url
        return CartItem.objects.select_related('product').filter(cart_id=self.kwargs['cart_pk'])

    """ def get_serializer_context(self):
         return {'card_id': self.kwargs['cart_id']}"""

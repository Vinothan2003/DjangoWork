from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count

from rest_framework.views import Response, status, APIView
from rest_framework.decorators import api_view
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

from store.models import Product, Collection, OrderItem
from store.serilaizer import ProductSerializer, CollectionSerializer


# Create your views here.

# -- VIEW-SET --
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

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

    """def deletes(self, request, pk):
        collection = get_object_or_404(
            Collection.objects.annotate(products_count=Count('products')),
            pk=pk)
        if collection.product.count() > 0:
            return Response(
                {'error': 'collection cannot be deleted because it is the foreign key for the product table'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)"""


"""# -- GENERICS --
class ProductList(ListCreateAPIView):  # --> get, post
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    # def get_queryset(self):    //  # ---> use when dealing with logic  //
    #     return Product.objects.select_related('collection').all()
    # 
    # def get_serializer(self, *args, **kwargs):  // # ---> use when dealing with logic  //
    #     return ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class ProductDetails(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # lookup_field = 'id'

    def deletes(self, request, id):
        product = get_object_or_404(Product, pk=id)  # getting product object
        if product.orderitems.count() > 0:  # if product have any order in the order item
            return Response({'error': 'this method is not allowed due some reasons.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# generics
class CollectionList(ListCreateAPIView):  # --> get, post
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def deletes(self, request, pk):
        collection = get_object_or_404(
            Collection.objects.annotate(products_count=Count('products')),
            pk=pk)
        if collection.product.count() > 0:
            return Response(
                {'error': 'collection cannot be deleted because it is the foreign key for the product table'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)"""

"""class ProductList(APIView):              # CLASS BASED VIEW
    def get(self, request):
        queryset = Product.objects.select_related('collection').all()  # get query set
        serializer = ProductSerializer(  # converting to dict using serializer
            queryset,
            many=True,
            context={'request': request})
        return Response(serializer.data)  # converting dict to json automatically

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # best , validating the data
        serializer.save()  # saving the data to db
        # print(serializer.validated_data) --> can see the validated data
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetails(APIView):              # CLASS BASED VIEW
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)  # getting product object
        serializer = ProductSerializer(product)  # object to dict
        return Response(serializer.data)  # dict to json

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)  # getting product object
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def deletes(self, request, id):
        product = get_object_or_404(Product, pk=id)  # getting product object
        if product.orderitems.count() > 0:  # if product have any order in the order item
            return Response({'error': 'this method is not allowed due some reasons.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(APIView):              # CLASS BASED VIEW

    def get(self, request):
        queryset = Collection.objects.annotate(products_count=Count('products')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CollectionDetail(APIView):              # CLASS BASED VIEW

    def get(self, request, pk):
        collection = get_object_or_404(
            Collection.objects.annotate(products_count=Count('products')),
            pk=pk)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)

    def put(self, request, pk):
        collection = get_object_or_404(
            Collection.objects.annotate(products_count=Count('products')),
            pk=pk)
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def deletes(self, request, pk):
        collection = get_object_or_404(
            Collection.objects.annotate(products_count=Count('products')),
            pk=pk)
        if collection.product.count() > 0:
            return Response(
                {'error': 'collection cannot be deleted because it is the foreign key for the product table'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) """

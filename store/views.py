from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from rest_framework.views import Response, status
from rest_framework.decorators import api_view

from store.models import Product, Collection
from store.serilaizer import ProductSerializer, CollectionSerializer

# Create your views here.

"""def product_list(request):  # --> DJANGO
    return HttpResponse('ok')"""


@api_view(['GET', 'POST'])
def product_list(request):  # --> REST FRAME-WORK
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()  # get query set
        serializer = ProductSerializer(  # converting to dict using serializer
            queryset,
            many=True,
            context={'request': request})
        return Response(serializer.data)  # converting dict to json automatically

    elif request.method == 'POST':  # DESERIALIZE
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # best , validating the data
        serializer.save()  # saving the data to db
        # print(serializer.validated_data) --> can see the validated data
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        #       (OR)
        # noinspection PyUnreachableCode
        """
        if serializer.is_valid():
            serializer.validated_data
            return Response('ok')
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        """


@api_view(['GET', 'PUT', 'DELETE'])
def product_details(request, id):  # best way
    product = get_object_or_404(Product, pk=id)  # getting product object
    if request.method == 'GET':
        serializer = ProductSerializer(product)  # object to dict
        return Response(serializer.data)  # dict to json

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if product.orderitems.count() > 0:  # if product have any order in the order item
            return Response({'error': 'this method is not allowed due some reasons.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    #        (OR)
    # noinspection PyUnreachableCode
    """ try:
            product = Product.objects.get(pk=id)  # get product object
            serializer = ProductSerializer(product)  # convert product object to dict
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  # OR (status=404) """


@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(products_count=Count('products')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(
        Collection.objects.annotate(products_count=Count('products')),
        pk=pk)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        if collection.product.count() > 0:
            return Response(
                {'error': 'collection cannot be deleted because it is the foreign key for the product table'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.views import Response, status
from rest_framework.decorators import api_view

from store.models import Product
from store.serilaizer import ProductSerializer

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

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # best , validating the data
        serializer.save()  # saving the data to db
        # print(serializer.validated_data) --> can see the validated data
        return Response('ok')
        #       (OR)
        # noinspection PyUnreachableCode
        """
        if serializer.is_valid():
            serializer.validated_data
            return Response('ok')
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        """


@api_view()
def product_details(request, id):  # best way
    product = get_object_or_404(Product, pk=id)  # getting product object
    serializer = ProductSerializer(product)  # object to dict
    return Response(serializer.data)  # dict to json
    #        (OR)
    # noinspection PyUnreachableCode
    """ try:
            product = Product.objects.get(pk=id)  # get product object
            serializer = ProductSerializer(product)  # convert product object to dict
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  # OR (status=404) """


@api_view()
def collection_detail(request, pk):
    return Response('ok')

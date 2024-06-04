from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product


def say_hello(request):
    # query_set = Product.objects.all()  # object --> manage object (remote controller) all() --> fetch all data from db
    """try:
        product = Product.objects.get(pk=0)
    except ObjectDoesNotExist:
        pass"""

    # query_set = Product.objects.filter(pk=0).first()  # get product object and return

    # exists = Product.objects.filter(pk=1).exists()  # return boolean value

    # first(), exists() --> return single product

    # queryset = Product.objects.filter(unit_price__gte=20).first() --> filtering objects

    # query_set = Product.objects.filter(unit_price__range=(20, 50)).order_by('unit_price')

    # query_set = Product.objects.filter(title__icontains='coffee')  # --> search using string
    # last_update__year=2021 --> year
    # description__isnull= True --> checking for null

    # -- complex lookups--
    # query_set = Product.objects.filter(unit_price__lt=20, inventory__lt=20) --> 1 - and
    # query_set = Product.objects.filter(inventory__gt=20).filter(unit_price__gt=20) --> 2 - and
    query_set = Product.objects.filter(
        Q(inventory__gt=20) | Q(unit_price__gt=20)).order_by("unit_price")  # 3 - or

    # Q(inventory__gt=20) | ~Q(unit_price__gt=20) --> 4 - ~not

    return render(request, 'hello.html', {'name': 'Vinothan NC', 'products': list(query_set)})

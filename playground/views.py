from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, OrderItem, Order


def say_hello(request):
    # query_set = Product.objects.all()  # object --> manage object (remote controller) all() --> fetch all data from db
    """try:
        product = Product.objects.get(pk=0)
    except ObjectDoesNotExist:
        pass"""
    #            (or)
    # query_set = Product.objects.filter(pk=0).first()  # get product object and return

    # exists = Product.objects.filter(pk=1).exists()  # return boolean value

    # first(), exists() --> return single product

    # queryset = Product.objects.filter(unit_price__gte=20).first() --> filtering objects

    # query_set = Product.objects.filter(unit_price__range=(20, 50)).order_by('unit_price')

    # query_set = Product.objects.filter(title__icontains='coffee')  # --> search using string
    # last_update__year=2021 --> year
    # description__isnull= True --> checking for null

    # --------------------------------------------------------------
    # -- complex lookups--
    # query_set = Product.objects.filter(unit_price__lt=20, inventory__lt=20) --> 1 - and
    # query_set = Product.objects.filter(inventory__gt=20).filter(unit_price__gt=20) --> 2 - and

    """ query_set = Product.objects.filter(
        Q(inventory__gt=20) | Q(unit_price__gt=20)).order_by("unit_price")  # 3 - or Q objects """

    # Q(inventory__gt=20) | ~Q(unit_price__gt=20) --> 4 - ~not

    # --------------------------------------------------------------
    # -- F objects---
    # query_set = Product.objects.filter(inventory=F('collection__id'))

    # --------------------------------------------------------------
    # --sorting--

    # query_set = Product.objects.order_by('unit_price', '-title').reverse()  # - ascending order
    # ('-unit_price') --> descending order
    # return render(request, 'hello.html', {'name': 'Vinothan NC', 'products': list(query_set)})
    # product = Product.objects.order_by('unit_price')[0]
    # product = Product.objects.earliest('unit_price') --> lowest
    # product = Product.objects.latest('unit_price')  # --> highest

    # return render(request, 'hello.html', {'name': 'Vinothan NC', 'product': product})

    # --------------------------------------------------------------
    # --Limit--

    # query_set = Product.objects.all()[:5]
    # query_set = Product.objects.all()[5:10]
    # return render(request, 'hello.html', {'name': 'Vinothan NC', 'products': list(query_set)})

    # --------------------------------------------------------------
    # --Selecting--

    # query_set = Product.objects.values('id', 'title', 'collection__title') --> gives dictionary
    # query_set = Product.objects.values_list('id', 'title', 'collection__title')  # --> list of tuple
    # query_set = Product.objects.filter(id__in=OrderItem.objects.values('product__id').distinct()).order_by('title')
    # return render(request, 'hello.html', {'name': 'Vinothan NC', 'products': query_set})

    # --------------------------------------------------------------
    # --deferring--

    # query_set = Product.objects.only('id', 'title')  # --> only needed fields

    # return render(request, 'hello.html', {'name': 'Vinothan NC', 'products': query_set})

    # query_set = Product.objects.defer('description')  # --> don't needed fields
    # return render(request, 'hello.html', {'name': 'Vinothan NC', 'products': query_set})

    # --------------------------------------------------------------
    # --selecting related field--

    # query_set = Product.objects.all()
    # select_related() --> 1 (one to many)
    # prefetch_related() --> n (many to many)

    # query_set = Product.objects.prefetch_related('promotion').select_related('collection').all()
    # return render(request, 'hello.html', {'name': 'Vinothan NC', 'products': list(query_set)})

    query_set = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at').all()[:5]
    return render(request, 'hello.html', {'name': 'Vinothan NC', 'orders': list(query_set)})

from django.shortcuts import render
from django.http import HttpResponse
from django.db import transaction, connection  # --> commit, rollback
from django.db.models import Q, F, DecimalField  # --> Q,F field
from django.db.models.aggregates import Count, Sum, Avg, Max, Min
from django.db.models.functions import Concat
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.db.models import Value, Func, ExpressionWrapper, DecimalField
from store.models import Product, OrderItem, Order, Customer, Collection
from tags.models import TaggedItem


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
    # query_set = Product.objects.filter(unit_price__lt=20, inventory__lt=20) --> 1 -> and (logical operator)
    # query_set = Product.objects.filter(inventory__gt=20).filter(unit_price__gt=20) --> 2 - and

    """ query_set = Product.objects.filter(
        Q(inventory__gt=20) | Q(unit_price__gt=20)).order_by("unit_price")  # 3 - or Q objects """

    # Q(inventory__gt=20) | ~Q(unit_price__gt=20) --> 4 - ~not

    # --------------------------------------------------------------
    # -- F objects---
    # query_set = Product.objects.filter(inventory=F('collection__id')) --> reference

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

    """query_set = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by(
        '-placed_at').all()[:5]
    return render(request, 'hello.html', {'name': 'Vinothan NC', 'orders': list(query_set)})"""

    # --------------------------------------------------------------
    # --Aggregate--
    """result = Product.objects.filter(collection__id= 1).aggregate(count=Count('id'), min_price=Max('unit_price'))
    return render(request, 'hello.html', {'name': 'Vinothan NC', 'result': result})"""

    # --------------------------------------------------------------
    # --Annotations, Value--

    # query_set = Customer.objects.annotate(is_new='True')  # cannot pass boolean value have to pass expression object
    # query_set = Customer.objects.annotate(is_new=Value(True))
    """query_set = Customer.objects.annotate(new_id=F('id') + 100)  # computation
    return render(request, 'hello.html', {'name': 'Vinothan NC', 'result': list(query_set)})"""

    # --------------------------------------------------------------
    # --Func--

    """queryset = Customer.objects.annotate(
        # CONCAT
        full_name=Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT')
        )"""
    # (or)
    """queryset = Customer.objects.annotate(
        # CONCAT
        full_name=Concat('first_name', Value(' '), 'last_name')
        
        return render(request, 'hello.html', {'name': 'Vinothan', 'result': list(queryset)})
    )"""

    # --------------------------------------------------------------
    # -- Group By--

    """queryset = Customer.objects.annotate(
        order_count=Count('order')
    )
    return render(request, 'hello.html', {'name': 'Vinothan NC', 'result': list(queryset)})"""

    # --------------------------------------------------------------
    # -- Expression wrapper--
    # use dealing with complex expression
    """discount = ExpressionWrapper(F('unit_price') - 0.8, output_field=DecimalField())
    queryset = Product.objects.annotate(

        # discount_price=F('unit_price') * 0.8 # show error because of complex expression
        discount_price=discount
    )
    return render(request, 'hello.html', {'name': 'Vinothan NC', 'result': list(queryset)})"""

    # --------------------------------------------------------------
    # -- query generic relationship--

    """content_type = ContentType.objects.get_for_model(Product)

    queryset = TaggedItem.objects \
        .filter(
            content_type=content_type,
            object_id=1
        )
    return render(request, 'hello.html', {'name': 'Vinothan NC', 'result': queryset})"""

    # --------------------------------------------------------------
    # -- queryset cache --

    """queryset = Product.objects.all()
    queryset[0]  # --> render new queryset 
    list(queryset)
    queryset[0]  # --> use the queryset cache
    return render(request, 'hello.html', {'name': 'Vinothan NC'})"""

    # --------------------------------------------------------------
    # -- creating field -- inserting values --

    """collection = Collection()
    collection.title = 'PC games'
    collection.featured_product = Product(pk=1)
    collection.save()

    return render(request, 'hello.html', {'name': 'Vinothan NC'})"""

    # --------------------------------------------------------------
    # -- updating field -- updating values --

    """collection = Collection(pk=11)
    collection.title = 'Video Games'  --> updating the both field
    collection.featured_product = Product(2)
    collection.save()"""

    """collection = Collection(pk=11)
        collection.featured_product = None --> django update the title field also 
        collection.save()"""

    """Collection.objects.filter(pk=11).update(featured_product=None)  # --> using this approach can update specific filed

    return render(request, 'hello.html', {'name': 'Vinothan NC'})"""

    # --------------------------------------------------------------
    # -- deleting field -- deleting values --

    """collection = Collection(pk=12)  # --> deleting the specific field
    collection.delete()

    Order.objects.filter(id__gt=1001).delete()  # getting queries and deleting some fields

    return render(request, 'hello.html', {'name': 'Vinothan NC'})"""

    # --------------------------------------------------------------
    # -- Transaction --

    # @transaction.atomic():  --> can use as annotation for whole function
    # def say_hello(request):

    """with transaction.atomic():  # for specific transaction
        order = Order()
        order.customer_id = 1
        order.save()

        item = OrderItem()
        item.order = order
        item.product_id = 1  # item.product_id = -1
        item.quantity = 2
        item.unit_price = 10
        order.save()

    return render(request, 'hello.html', {'name': 'Vinothan NC'})"""

    # --------------------------------------------------------------
    # -- Executing raw sql  --
    # use when dealing with complex queries

    """queryset = Product.objects.raw(
        "SELECT * FROM store_product")"""  # this queryset this different form comparing to other queryset

    """ with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM store_customer')   # there is no limit for writing query

    return render(request, 'hello.html', {'name': 'Vinothan NC', 'result': list(queryset)}) """

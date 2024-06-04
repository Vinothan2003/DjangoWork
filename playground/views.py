from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product


def say_hello(request):
    # query_set = Product.objects.all()  # object --> manage object (remote controller) all() --> fetch all data from db
    """try:
        product = Product.objects.get(pk=0)
    except ObjectDoesNotExist:
        pass"""

    # query_set = Product.objects.filter(pk=0).first()  # get product object and return

    exists = Product.objects.filter(pk=1).exists()  # return boolean value

    return render(request, 'hello.html', {'name': 'Vinothan NC'})

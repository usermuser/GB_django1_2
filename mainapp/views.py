from django.shortcuts import render
from django.urls import resolve
from django.http import HttpRequest, HttpResponseRedirect
from .models import ProductCategory, Product
import json
import datetime

now = datetime.datetime.now()
current_year = now.year


def categories(request, pk=None):
    if pk is None:
        return HttpResponseRedirect('/')
    else:
        categories = ProductCategory.objects.order_by('name')
        current_category=ProductCategory.objects.get(pk=pk)
        ctx = {'categories':categories,
               'current_category': current_category, }
        return render(request, 'mainapp/category.html', ctx)

def index(request):
    current_url = resolve(request.path_info).url_name
    title = 'Главная'

    ctx = {'title': title,
           'current_year': current_year,
           'current_url': current_url,
           'products': products}

    return render(request, 'mainapp/index.html', ctx)


def products(request, pk=None):
    title = 'Каталог'
    categories = ProductCategory.objects.order_by('name')
    if pk is not None:
        products = Product.objects.filter(pk=pk)
    else:
        products = Product.objects.order_by('-price')

    ctx = {'title': title,
           'categories': categories,
           'products':products,
           'current_year': current_year, }

    return render(request, 'mainapp/products.html', ctx)


def contact(request):
    title = 'Контакты'

    ctx = {'title': title,
           'current_year': current_year, }

    return render(request, 'mainapp/contact.html', ctx)

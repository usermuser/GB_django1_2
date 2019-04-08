from django.shortcuts import render
from django.urls import resolve
from django.http import HttpResponse, HttpResponseRedirect
from .models import ProductCategory, Product
from django.shortcuts import get_object_or_404
import datetime


now = datetime.datetime.now()
current_year = now.year

def seed_db(request): # это код больше не нужен, делаю через management
    ProductCategory.objects.all().delete()
    Product.objects.all().delete()

    cat1 = ProductCategory()
    cat1.name = 'категория1'
    cat1.description = 'описания категории 1 бла бла бла 12314123'
    cat1.save()

    prod1 = Product()
    prod1.name = 'product1 имя'
    prod1.category = cat1
    prod1.save()

    print('[+] Created {}, {}'.format(cat1.name, prod1.name))

    cat2 = ProductCategory()
    cat2.name = 'категория22222'
    cat2.description = 'описаия егории 2 22222222222 бла 12314123'
    cat2.save()

    prod2 = Product()
    prod2.name = 'prod222222222'
    prod2.category = cat2
    prod2.save()

    print('[+] Created {}, {}'.format(cat2.name, prod2.name))
    return HttpResponse('<h1> Done! </h1> ')



def categories(request, pk=None):
    if pk is None:
        return HttpResponseRedirect('/')
    else:
        categories = ProductCategory.objects.order_by('name')
        current_category = ProductCategory.objects.get(pk=pk)
        ctx = {'categories': categories,
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
    title = 'продукты'
    categories = ProductCategory.objects.order_by('name')

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        ctx = {'title': title,
               'categories': categories,
               'category': category,
               'products': products,
               'current_year': current_year, }

        return render(request, 'mainapp/products.html', ctx)

    same_products = Product.objects.all()[3:5]

    ctx = {
        'title': title,
        'categories': categories,
        'same_products': same_products,}

    return render(request, 'mainapp/products.html', ctx)


def contact(request):
    title = 'Контакты'

    ctx = {'title': title,
           'current_year': current_year, }

    return render(request, 'mainapp/contact.html', ctx)

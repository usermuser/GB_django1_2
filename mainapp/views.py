from django.shortcuts import render
from django.urls import resolve
import json
import datetime

now = datetime.datetime.now()
current_year = now.year


def index(request):
    title = 'Главная'
    current_url = resolve(request.path_info).url_name
    ctx = {'title': title,
           'current_year': current_year,
           'current_url': current_url, }

    return render(request, 'mainapp/index.html', ctx)


def products(request):
    with open ('docs/links_menu.json') as data:
        links_menu = json.load(data)

    title = 'Каталог'
    ctx = {'title': title,
           'links_menu': links_menu,
           'current_year': current_year, }

    return render(request, 'mainapp/products.html', ctx)


def contact(request):
    title = 'Контакты'
    ctx = {'title': title,
           'current_year': current_year, }

    return render(request, 'mainapp/contact.html', ctx)

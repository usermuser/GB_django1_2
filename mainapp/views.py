from django.shortcuts import render
import json

def index(request):
    title = 'Главная'
    ctx = {'title': title,}
    return render(request, 'mainapp/index.html', ctx)

def products(request):
    with open ('docs/links_menu.json') as data:
        links_menu = json.load(data)

    print(links_menu)
    title = 'Каталог'
    ctx = {'title': title,
           'links_menu': links_menu,
           }
    return render(request, 'mainapp/products.html', ctx)

def contact(request):
    title = 'Контакты'
    ctx = {'title': title,
           }
    return render(request, 'mainapp/contact.html', ctx)

from django.shortcuts import render

def index(request):
    title = 'жопа'
    ctx = {'title': title,}
    return render(request, 'mainapp/index.html', ctx)

def products(request):
    return render(request, 'mainapp/products.html')

def contact(request):
    return render(request, 'mainapp/contact.html')

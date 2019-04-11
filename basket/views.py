from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from basket.models import Basket
from mainapp.models import Product

# просмотр корзины
def basket(request):
    ctx = {}
    return render(request, 'basketapp/basket.html', ctx)

# добавить товар в корзину, сначала найдя его по pk
def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    # если корзины у пользователя еще нет
    # создаем корзину
    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# удалить товар из корзины
def basket_remove(request, pk):
    ctx = {}
    return render(request, 'basketapp/basket.html', ctx)

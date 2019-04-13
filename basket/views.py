from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from basket.models import Basket
from mainapp.models import Product

from django.contrib.auth.decorators import login_required
from django.urls import reverse


# просмотр корзины
@login_required
def basket(request):
    title = 'корзина'
    basket_items = Basket.objects.filter(user=request.user).\
                                    order_by('product__category')
    print('basket items: ', basket_items)

    ctx = {'title': title,
           'basket_items': basket_items}

    return render(request, 'basket/basket.html', ctx)


# добавить товар в корзину, сначала найдя его по pk
@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('mainapp:product', args=[pk]))
    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    # если корзины у пользователя еще нет
    # создаем корзину и добавляем туда product
    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# dont forget to add check if request is post and add csrf
@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

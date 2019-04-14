from django.shortcuts import render
from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render
from mainapp.models import ProductCategory, Product


def users(request):
    title = 'админка/пользователи'

    users_list = ShopUser.objects.all().order_by('-is_active', '-is.superuser',
                                                 '-is.staff', 'username')

    ctx = {
        'title': title,
        'users_list': users_list,
    }

    return render(request, 'adminapp/users.html', ctx)


def user_create(request):
    pass


def user_update(request, pk):
    pass


def user_delete(request, pk):
    pass


def categories(request):
    title = 'админка/категории'

    categoriest_list = ProductCategory.objects.all().order_by('-name')

    ctx = {'categories_list': categoriest_list}
    return render(request, 'adminapp/categories.html', ctx)

def category_create(request):
    pass


def category_update(request):
    pass


def category_delete(request):
    pass


def products(request, pk):  # note that is category pk!
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    ctx = {
        'title': title,
        'category': category,
        'products_list': products_list,
    }

    return render(request, 'adminapp/products.html', ctx)


def product_create(request, pk):
    pass


def product_read(request, pk):
    pass


def product_update(request, pk):
    pass


def product_delete(request, pk):
    pass














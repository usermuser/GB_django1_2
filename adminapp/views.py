from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from authapp.models import ShopUser
from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ShopUserAdminEditForm
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import user_passes_test
from mainapp.models import ProductCategory, Product


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'админка/пользователи'

    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser',
                                                 '-is_staff', 'username')

    ctx = {
        'title': title,
        'users_list': users_list,
    }

    return render(request, 'adminapp/users.html', ctx)


def user_create(request):
    title = 'пользователи/создание'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        user_form = ShopUserRegisterForm()

    ctx = {'title': title, 'update_form': user_form}

    return render(request, 'adminapp/user_update.html', ctx)


def user_update(request, pk):
    title = 'пользователи/редкатирование'

    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES,
                                          instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:user_update',
                                                args=[edit_user.pk]))
    else:
        edit_form = ShopUserAdminEditForm(isinstance=edit_user)

    ctx = {'title': title, 'update_form': edit_form,}

    return render(request, 'adminapp/user_update.html', ctx)


def user_delete(request, pk):
    title = 'пользователи/удаление'

    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        # user.delete()
        # вместо удаления лучше сделаем неактивным
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('admin:users'))

    content = {'title': title, 'user_to_delete': user}

    return render(request, 'adminapp/user_delete.html', content)


def categories(request):
    title = 'админка/категории'

    categoriest_list = ProductCategory.objects.all().order_by('-name')

    ctx = {
        'categories_list': categoriest_list
    }

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














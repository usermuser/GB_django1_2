from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserChangeForm
from django.contrib import auth
from django.urls import reverse


def login(request):
    title = 'вход'

    login_form = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('mainapp:all_products_descending_order'))

    ctx = {'title': title, 'login_form': login_form}
    return render(request, 'authapp/login.html', ctx)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('authapp:login'))
    else:
        register_form = ShopUserRegisterForm


    ctx = {'title': title, 'register_form': register_form}

    return render(request, 'authapp/register.html', ctx)



def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = ShopUserChangeForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('authapp:edit'))
    else:
        edit_form = ShopUserChangeForm(instance=request.user)

    ctx = {'title': title, 'edit_form': edit_form}

    return render(request, 'authapp/edit.html', ctx)



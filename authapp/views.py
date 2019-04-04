from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForm
from django.contrib import auth
from django.urls import reverse


def login(request):
    title = 'вход'

    login_form = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST', and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main'))

        ctx = {'title':title, 'login_form':login_form}
        return render(request, 'authapp/login.html', ctx)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


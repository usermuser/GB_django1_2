from django.shortcuts import render, HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import auth
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotFound

from authapp.models import ShopUser
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserChangeForm


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verification.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user: {e.args}')
        return HttpResponseRedirect(reverse('mainapp:index'))


def send_verify_email(user):
    verify_link = reverse('auth:verify', kwargs={
                              'email': user.email,
                              'activation_key': user.activation_key
                          })

    title = f'Подтверждение учетной записи {user.username}'

    msg = f'Для подтверждения учетной записи {user.username} на портале \
        {settings.DOMAIN_NAME} перейдите по ссылке: \
        \n{settings.DOMAIN_NAME}{verify_link}'

    # send_mail function returning quantity of sent messages
    return send_mail(title, msg, settings.EMAIL_HOST_USER, [user.email],
                     fail_silently=False)


def login(request):
    title = 'вход'
    login_form = ShopUserLoginForm()
    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST':
        login_form = ShopUserLoginForm(data=request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                if 'next' in request.POST.keys():
                    return HttpResponseRedirect(request.POST['next'])
                else:
                    return HttpResponseRedirect(reverse('mainapp:index'))

    ctx = {'title': title,
           'login_form': login_form,
           'next': next,}
    return render(request, 'authapp/login.html', ctx)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):
    title = 'регистрация'
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():

            user = register_form.save()

            if send_verify_email(user):
                print('сообщение подтверждения отправлено')
                return HttpResponseRedirect(reverse('mainapp:index'))
            else:
                print('Ошибка отправки сообщения')
                return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    ctx = {'title': title, 'register_form': register_form,}
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



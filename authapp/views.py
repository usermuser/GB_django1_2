from django.shortcuts import render, HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import auth
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotFound

from authapp.models import ShopUser
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserChangeForm

def verify(request):
    pass


def send_verify_email(user):
    print(f'user.email is {user.email} and actkey is {user.activation_key}') # почему тут ключ пуст?
    verify_link = reverse('auth:verify', kwargs={
                              'email': user.email,
                              'activation_key': user.activation_key
                              # 'activation_key': 'ne rabotaet'
                          })



    # verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    title = f'Подтверждение учетной записи {user.name}'

    msg = f'Для подтверждения учетной записи {user.usernam} на портале \
        {settings.DOMAIN_NAME} перейдите по ссылке: \
        \n{settings.DOMAIN_NAME}{verify_link}'

    # send_mail function returning quantity of sent messages
    return send_mail(title, msg, settings.EMAIL_HOST_USER, [user.email],
                     fail_silently=False)


def login(request):
    title = 'вход'

    login_form = ShopUserLoginForm(data=request.POST)

    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and login_form.is_valid():
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
            print('form is valid')

            user = register_form.save()
            print('form is saved')

            print('user.email: ', user.email)
            print('user.actkey: ', user.activation_key) # вот тут пусто

            if send_verify_email(user):
                print('сообщение подтверждения отправлено')
                # return HttpResponseRedirect(reverse('main')) # разное пробовал тут
                # return HttpResponseRedirect(reverse('auth:login'))
                return HttpResponse('<h1> Message sent succesfully </h1>')
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



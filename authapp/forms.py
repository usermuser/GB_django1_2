import random
import hashlib

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms

from authapp.models import ShopUser


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'password1', 'password2', 'email', 'age', 'avatar')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                field.help_texts = ''

        # def clean_age(self):
        #     data = self.cleaned_data['age']
        #     if data < 18:
        #         raise forms.ValidationError('Вы слишком молоды!')
        #
        #     return data

        # возможно в этом дело
        # def too_old(self):
        #     data = self.too_old['age']
        #     if data > 70:
        #         raise forms.ValidationError('Вы слишком стары!')
        #
        # def is_num(self):
        #     data = self.too_old['age']
        #     if not isinstance(data, int):
        #         raise forms.ValidationError('Введите число!')

        def save(self):
            user = super().save() # этот вариант пробовал, проблему не решило
            # user = super(ShopUserRegisterForm, self).save()

            user.is_active = False

            # creating salt
            salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]

            user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
            # user.activation_key = '246' # положим сюда 246
            print('Думаю тут будет пусто:', user.activation_key) # эта строчка не печатается
            user.save()

            return user

# это скопировал из методички и это тоже не помогло
#         def save(self):
#             user = super(ShopUserRegisterForm, self).save()
#
#             user.is_active = False
#             salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
#             user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
#             user.save()
#
#             return user


class ShopUserChangeForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'email', 'age', 'avatar', 'password')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                field.help_texts = ''
                if field_name == 'password':
                    field.widget = forms.HiddenInput()

        def clean_age(self):
            data = self.cleaned_data['age']
            if data < 18:
                raise forms.ValidationError('Вы слишком молоды!')

            return data


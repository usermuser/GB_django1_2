from django.urls import path, include

import mainapp.views as mainapp


app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.products, name='index'),  # show products
    path('<int:pk>', mainapp.products, name='category'),
    path('product/<int:pk>/', mainapp.product, name='product'),  # show product details
]


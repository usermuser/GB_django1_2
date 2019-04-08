from django.urls import path

from mainapp import views


app_name = 'mainapp'

urlpatterns = [
    path('', views.products, name='all_products_descending_order'),
    path('<int:pk>', views.products, name='product'),
    path('category/<int:pk>', views.categories, name='category'),
]

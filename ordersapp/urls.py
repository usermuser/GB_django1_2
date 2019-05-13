from django.urls import path, re_path

from ordersapp import views


app_name = 'ordersapp'

urlpatterns = [
    re_path(r'^orders_all', views.OrderList.as_view(), name='orders_all'),

]

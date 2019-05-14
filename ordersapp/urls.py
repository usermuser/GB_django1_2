from django.urls import path, re_path

from ordersapp import views


app_name = 'ordersapp'

urlpatterns = [
    re_path(r'^orders_all$', views.OrderList.as_view(), name='orders_all'),
    re_path(r'^order_create/$', views.OrderItemsCreate.as_view(), name='create_order'),
    re_path(r'^order_update/(?P<pk>\w+)/$', views.OrderItemsUpdate.as_view(), name='update_order'),
    re_path(r'^order_delete/(?P<pk>\w+)/$', views.OrderItemsDelete.as_view(), name='delete_order'),
    re_path(r'^order_detail/(?P<pk>\w+)/$', views.OrderRead.as_view(), name='read_order'),
    re_path(r'^order_forming_complete/(?P<pk>\w+)/$', views.order_forming_complete, name='order_forming_complete'),

]

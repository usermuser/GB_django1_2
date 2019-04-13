from django.urls import path

from basket import views

app_name = 'basket'

urlpatterns = [
    path('', views.basket, name='view'),
    path('add/<int:pk>/', views.basket_add, name='add'),
    path('remove/<int:pk>/', views.basket_remove, name='remove'),
]

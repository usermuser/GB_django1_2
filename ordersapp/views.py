from urllib import request

from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem


# def ordering_main(request):
#     pass

class OrderList(ListView):
   model = Order

   def get_queryset(self):
       return Order.objects.filter(user=self.request.user)


class OrderItemsCreate(CreateView):
   model = Order
   fields = []
   # form_class = OrderForm  # another way to pull fields
   success_url = reverse_lazy('ordersapp:orders_all')

   def get_context_data(self, **kwargs):
       data = super(OrderItemsCreate, self).get_context_data(**kwargs)
       OrderFormSet = inlineformset_factory(Order, OrderItem,
                                            form=OrderItemForm,
                                            extra=1)

       if self.request.POST:
           formset = OrderFormSet(self.request.POST, self.request.FILES)
       else:
           # basket_items = Basket.get_items(self.request.user) # original
           basket_items = self.request.user.basket.all()
           if len(basket_items):
               OrderFormSet = inlineformset_factory(Order, OrderItem,
                                                    form=OrderItemForm,
                                                    extra=len(basket_items))
               formset = OrderFormSet()
               for num, form in enumerate(formset.forms):
                   form.initial['product'] = basket_items[num].product
                   form.initial['quantity'] = basket_items[num].quantity
               # basket_items.delete() # это нужно делать в другом месте, позже, когда заказ создан
               # смотри метод form_valid ниже по коду.
           else:
               formset = OrderFormSet()

       data['orderitems'] = formset
       return data

   def form_valid(self, form):
       context = self.get_context_data()
       orderitems = context['orderitems']

       with transaction.atomic():
           form.instance.user = self.request.user
           self.object = form.save()
           if orderitems.is_valid():
               orderitems.instance = self.object
               orderitems.save()
           self.request.user.basket.all().delete()
       # # удаляем пустой заказ
       # if self.object.get_total_cost() == 0:
       #     self.object.delete()

       return super().form_valid(form)

from django.urls import path
from .views import orders_list, order_checkout

urlpatterns = [
    path('', orders_list, name='orders_list'),
    path('checkout/<int:id>/', order_checkout, name='order_checkout'),
]
from .views import shipping, checkout, complete_order, payment_success, payment_fail
from django.urls import path

app_name = 'payment'

urlpatterns = [
    path('shipping/', shipping, name='shipping'),
    path('checkout/', checkout, name='checkout'),
    path('complete-order', complete_order, name='complete_order'),
    path('payment-success/', payment_success, name='payment_success'),
    path('payment-fail/', payment_fail, name='payment_fail'),
]
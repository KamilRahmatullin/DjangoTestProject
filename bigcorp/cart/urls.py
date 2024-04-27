from django.urls import path
from .views import cart_view, cart_add, cart_update, cart_delete

app_name = 'cart'

urlpatterns = [
    path('', cart_view, name='cart_view'),
    path('add/', cart_add, name='add_to_cart'),
]
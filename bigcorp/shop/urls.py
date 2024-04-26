from django.urls import path
from .views import products_view, product_detail_view, category_list_view

app_name = 'shop'

urlpatterns = [
    path('', products_view, name='products'),
    path('<slug:slug>/', product_detail_view, name='product_detail'),
    path('<slug:slug>/', category_list_view, name='category_list'),
]

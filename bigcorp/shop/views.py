from django.shortcuts import render, get_object_or_404

from .models import Category, ProductProxy


def products_view(request):
    products = ProductProxy.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'shop/products.html', context)


def product_detail_view(request, slug):
    product = get_object_or_404(ProductProxy, slug=slug)
    context = {
        'product': product,
    }
    return render(request, 'shop/product_detail.html', context)


def category_list_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = ProductProxy.objects.filter(category=category)
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'shop/category_list.html', context)

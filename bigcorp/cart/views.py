from django.shortcuts import render, get_object_or_404

from cart.cart import Cart
from shop.models import ProductProxy
from django.http import JsonResponse


def cart_view(request):
    return render(request, 'cart/cart_view.html')


def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(ProductProxy, id=product_id)
        cart.add(product=product, quantity=product_qty)
        cart_qty = cart.__len__()

        response = JsonResponse({'cart_qty': cart_qty, 'product': product.title})
        return response


def cart_update(request):
    ...


def cart_delete(request):
    cart = Cart(request)

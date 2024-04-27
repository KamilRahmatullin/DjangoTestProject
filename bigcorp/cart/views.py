from django.shortcuts import render, get_object_or_404

from cart.cart import Cart
from shop.models import ProductProxy
from django.http import JsonResponse


def cart_view(request):
    cart = Cart(request)

    context = {
        'cart': cart
    }
    return render(request, 'cart/cart_view.html', context=context)


def cart_add(request):
    """
    Add a product to the cart and return a JSON response with the updated cart quantity and the product title.

    Parameters:
    - request: HttpRequest object containing the POST data with 'action', 'product_id', and 'product_qty' fields.

    Returns:
    - JsonResponse: JSON response containing the updated cart quantity and the title of the added product.
    """
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

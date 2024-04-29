from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from cart.cart import Cart

from .forms import ShippingAddressForm
from .models import ShippingAddress, Order, OrderItem


@login_required(login_url='account:login')
def shipping(request):
    try:
        shipping_address = ShippingAddress.objects.get(user=request.user)
    except ShippingAddress.DoesNotExist:
        shipping_address = None

    form = ShippingAddressForm(instance=shipping_address)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=shipping_address)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            return redirect('account:dashboard')
    return render(request, 'payment/shipping.html', {'form': form})


def checkout(request):
    # return render(request, 'payment/checkout.html')
    ...


def complete_order(request):
    # return render(request, 'payment/complete_order.html')
    ...


def payment_success(request):
    # return render(request, 'payment/payment_success.html')
    ...


def payment_fail(request):
    # return render(request, 'payment/payment_failure.html')
    ...

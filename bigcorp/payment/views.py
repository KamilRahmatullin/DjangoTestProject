import stripe
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from decimal import Decimal

from cart.cart import Cart

from .forms import ShippingAddressForm
from .models import ShippingAddress, Order, OrderItem

from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


@login_required(login_url='account:login')
def shipping(request):
    """
    View function for handling shipping address form submission and rendering the shipping address form page.

    Returns:
    - If the request method is 'POST' and the form is valid, it saves the shipping address and redirects to the dashboard page.
    - If the request method is 'GET' or the form is invalid, it renders the shipping address form page with the form data.

    This function retrieves the shipping address for the current user, populates the shipping address form with the retrieved data,
    and processes the form submission. If the form is valid, it saves the shipping address and redirects to the dashboard page.
    if the form is invalid or the request method is 'GET', it renders the shipping address form page with the form data.
    """
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


@login_required(login_url='account:login')
def checkout(request):
    """
    View function for handling the checkout process.

    This function checks if the user is authenticated and retrieves the shipping address for the user.
    If the user is authenticated and a shipping address exists,
    it renders the checkout page with the shipping address. If the user is not authenticated or no shipping address
    exists, it renders the checkout page without the shipping address.
    """
    if request.user.is_authenticated:
        shipping_address = get_object_or_404(ShippingAddress, user=request.user)
        if shipping_address:
            return render(request, 'payment/checkout.html', {'shipping_address': shipping_address})
    return render(request, 'payment/checkout.html')


def complete_order(request):
    """
    Handles the completion of an order, including creating a new order, associating it with the user and their shipping address,
    and creating order items for the products in the cart.

    This function retrieves the user's payment and shipping information from the POST request data, creates a new shipping address
    or retrieves an existing one, calculates the total price of the items in the cart, and then creates a new order and order items
    based on this information. If the user is authenticated, the order is associated with the user, otherwise, it is created without
    a user association. Finally, it returns a JSON response indicating the success of the order completion.
    """
    if request.method == 'POST':
        payment_type = request.POST.get('stripe-payment', 'yookassa-payment')

        name = request.POST.get('name')
        email = request.POST.get('email')
        street_address = request.POST.get('street_address')
        apartment_address = request.POST.get('apartment_address')
        city = request.POST.get('city')
        country = request.POST.get('country')
        zip_code = request.POST.get('zip_code')
        cart = Cart(request)
        total_price = cart.get_total_price()

        match payment_type:
            case 'stripe-payment':
                shipping_address, _ = ShippingAddress.objects.get_or_create(
                    user=request.user,
                    defaults={
                        'full_name': name,
                        'email': email,
                        'street_address': street_address,
                        'apartment_address': apartment_address,
                        'city': city,
                        'country': country,
                        'zip_code': zip_code,
                    }
                )
                session_data = {
                    'mode': 'payment',
                    'success_url': request.build_absolute_uri(reverse('payment:payment_success')),
                    'cancel_url': request.build_absolute_uri(reverse('payment:payment_fail')),
                    'line_items': []
                }

                if request.user.is_authenticated:
                    order = Order.objects.create(user=request.user, shipping_address=shipping_address,
                                                 total_price=total_price)

                    for item in cart:
                        OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                                 quantity=item['quantity'], user=request.user)
                        session_data['line_items'].append({
                            'price_data': {
                                'unit_amount': int(item['price'] * Decimal(100)),
                                'currency': 'usd',
                                'product_data': {
                                    'name': item['product'].title,
                                },
                            },
                            'quantity': item['quantity'],
                        })

                        session_data['client_reference_id'] = order.id
                        session = stripe.checkout.Session.create(**session_data)
                        return redirect(session.url, code=303)
                else:
                    order = Order.objects.create(shipping_address=shipping_address, total_price=total_price)

                    for item in cart:
                        OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                                 quantity=item['quantity'])
    return JsonResponse({'success': True})


def payment_success(request):
    """
    View function for handling a successful payment.

    This function clears the session data to remove any sensitive information related to the payment,
    and then renders the payment success page.
    """
    for key in list(request.session.keys()):
        del request.session[key]
    return render(request, 'payment/payment_success.html')


def payment_fail(request):
    return render(request, 'payment/payment_fail.html')

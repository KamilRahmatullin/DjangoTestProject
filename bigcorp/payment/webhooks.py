from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe

from .models import Order
from .tasks import send_order_confirmation


@csrf_exempt
def stripe_webhook(request):
    """
    Handle the Stripe webhook for processing payment events.

    Parameters:
    - request: The HTTP request object containing the webhook data.

    Returns:
    - HttpResponse: HTTP response indicating the status of the webhook processing.

    This function is responsible for processing the incoming Stripe webhook request. It verifies the signature,
    constructs the event, and processes the checkout session completed event to update the order status and send
    confirmation emails.
    """
    if request.method == 'POST':
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            if session.mode == 'payment' and session.payment_status == 'paid':
                try:
                    order_id = session.client_reference_id
                except Order.DoesNotExist:
                    return HttpResponse(status=404)

                send_order_confirmation.delay(order_id)
                order = Order.objects.get(id=order_id)
                order.paid = True
                order.save()

        return HttpResponse(status=200)

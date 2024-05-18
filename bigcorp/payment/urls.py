from .views import shipping, checkout, complete_order, payment_success, payment_fail, admin_order_pdf
from django.urls import path
from .webhooks import stripe_webhook

app_name = 'payment'

urlpatterns = [
    path('shipping/', shipping, name='shipping'),
    path('checkout/', checkout, name='checkout'),
    path('complete-order', complete_order, name='complete_order'),
    path('payment-success/', payment_success, name='payment_success'),
    path('payment-fail/', payment_fail, name='payment_fail'),
    path('webhook-stripe/', stripe_webhook, name='webhook_stripe'),
    path("order/<int:order_id>/pdf/", admin_order_pdf, name="admin_order_pdf"),
]
from django.urls import path
from checkout.views import Checkout, CheckoutSuccess

# The webhook() function will live in a file called "webhooks.py"
from .webhooks import webhook

urlpatterns = [
    path("", Checkout.as_view(), name="checkout"),
    path(
        "checkout-success/<order_number>",
        CheckoutSuccess.as_view(),
        name="checkoutSuccess",
    ),
    path("wh/", webhook, name="webhook"),
]
# Path "wh/" will return a function called "webhook()" with the name of "webhook"

from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.urls.base import reverse
from checkout.forms import OrderForm
from bag.contexts import bag_contents
from boutique_ado.settings import (
    STRIPE_PUBLIC_KEY,
    STRIPE_SECRET_KEY,
    STRIPE_CURRENCY,
)

import stripe


class Checkout(TemplateView):
    def get(self, request):
        stripe_public_key = STRIPE_PUBLIC_KEY
        stripe_secret_key = STRIPE_SECRET_KEY

        bag = request.session.get("bag", {})

        # Bag is empty
        if not bag:
            messages.error(request, "There's nothing in your bag")
            # This will prevent people from manually accessing the URL
            # by typing "/checkout"
            return redirect(reverse("products"))

        # Pass in the request and get the bag dictionary
        current_bag = bag_contents(request)
        # Retrieve the grand total from the current bag
        total = current_bag["grand_total"]
        # Stripe requires the amount to charge to be an integer
        stripe_total = round(total * 100)

        stripe.api_key = stripe_secret_key
        # Create the payment intent giving it the amount and the currency
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=STRIPE_CURRENCY,
        )

        print(intent.client_secret)

        # An instance of our order form - which will be empty for now.
        order_form = OrderForm()

        if not stripe_public_key:
            messages.warning(
                request,
                "Stripe public key is missing.  Did you forget to set it in your environment?",
            )
        # The template
        template_name = "checkout/checkout.html"
        # Context containing the order form.
        context = {
            "order_form": order_form,
            "stripe_public_key": stripe_public_key,
            "client_secret": intent.client_secret,
        }

        return render(request, template_name, context)

from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.urls.base import reverse
from checkout.forms import OrderForm


class Checkout(TemplateView):
    def get(self, request):
        bag = request.session.get("bag", {})

        # Bag is empty
        if not bag:
            messages.error(request, "There's nothing in your bag")
            # This will prevent people from manually accessing the URL
            # by typing "/checkout"
            return redirect(reverse("products"))

        # An instance of our order form - which will be empty for now.
        order_form = OrderForm()
        # The template
        template_name = "checkout/checkout.html"
        # Context containing the order form.
        context = {
            "order_form": order_form,
            "stripe_public_key": "pk_test_51LTZcpIYwD1Sv5tNNF2yHlPgyxmjvxChh3i4eBhb1ISyZq7NjNDJzFeRgWDmf0thkPkDkN5g7IvXQ1kYVJ1N7pDg008nH17kl8",
            "client_secret": "Test client secret",
        }

        return render(request, template_name, context)

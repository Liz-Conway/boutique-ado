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
        }

        return render(request, template_name, context)

from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.template import context
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from django.contrib import messages
from checkout.models import Order


class ProfileView(TemplateView):
    """
    Display the user's profile
    """

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=request.user)

        # Populate form with the user's current profile information
        form = UserProfileForm(instance=profile)
        # Will be rendering an order history on this page.
        # Use the profile and the related name on the order model
        # to get the users orders and return those to the template
        orders = profile.orders.all()

        template_name = "profiles/profile.html"
        context = {
            "form": form,
            "orders": orders,
        }

        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=request.user)

        # Create a new instance of the UserProfileForm using the POST data.
        # Tell it the instance we're updating is the profile we've just retrieved above
        form = UserProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")

        # Will be rendering an order history on this page.
        # Use the profile and the related name on the order model
        # to get the users orders and return those to the template
        orders = profile.orders.all()

        template_name = "profiles/profile.html"
        context = {"form": form, "orders": orders, "on_profile_page": True}

        return render(request, template_name, context)


class OrderHistory(TemplateView):
    def get(self, request, order_number):
        # Get the order
        order = get_object_or_404(Order, order_number=order_number)

        # Add a message letting the user know they're looking at a past order confirmation
        messages.info(
            request,
            f"This is a past confirmation for order number :  {order_number}."
            "A confirmation email was sent on the order date.",
        )

        # Use the checkout success template
        # since that template already has the layout for rendering a nice order confirmation
        template_name = "checkout/checkoutSuccess.html"

        # Add another variable to the context called "from_profile"
        # So we can check in the template if the user got there via the order history view
        context = {"order": order, "from_profile": True}

        return render(request, template_name, context)

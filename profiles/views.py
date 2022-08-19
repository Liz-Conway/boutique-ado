from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.template import context
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from django.contrib import messages


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

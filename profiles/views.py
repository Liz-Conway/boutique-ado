from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.template import context
from profiles.models import UserProfile


class ProfileView(TemplateView):
    """
    Display the user's profile
    """

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=request.user)

        template_name = "profiles/profile.html"
        context = {"profile": profile}

        return render(request, template_name, context)

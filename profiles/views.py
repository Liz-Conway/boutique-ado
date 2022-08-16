from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.template import context


class ProfileView(TemplateView):
    """
    Display the user's profile
    """

    def get(self, request, *args, **kwargs):
        template_name = "profiles/profile.html"
        context = {}

        return render(request, template_name, context)

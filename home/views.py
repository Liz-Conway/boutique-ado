from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import request

# Create your views here.
class HomePage(TemplateView):
    """ A class for rendering the home page """
    template_name = 'home/index.html'
    
    def get(self, request):
        return render(request, self.template_name)
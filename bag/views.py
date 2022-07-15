from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class BagContents(TemplateView):
    """ A class for rendering the bag contents page """
    template_name = 'bag/bag.html'
    
    def get(self, request):
        return render(request, self.template_name)
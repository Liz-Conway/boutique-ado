from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Product
# from django.template import context

# Create your views here.
class AllProducts(TemplateView):
    """ 
    A class show all products,
    including sorting and search queries
     """
    template_name = 'products/products.html'
    
    def get(self, request):
        products = Product.objects.all()
        
        context = {
            'products': products,
        }
    
        return render(request, self.template_name, context)
    
    
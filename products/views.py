from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from .models import Product
# from django.template import context


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

    
class ProductDetail(TemplateView):
    """ 
    A class show all individual product details
     """
    template_name = 'products/product-details.html'
    
    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        
        context = {
            'product': product,
        }
    
        return render(request, self.template_name, context)
    
    
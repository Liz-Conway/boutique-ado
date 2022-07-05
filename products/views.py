from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from .models import Product
from django.contrib import messages
from django.urls.base import reverse
from django.db.models.query_utils import Q
from products.models import Category
# from django.template import context


class AllProducts(TemplateView):
    """ 
    A class show all products,
    including sorting and search queries
     """
    template_name = 'products/products.html'
    
    def get(self, request):
        products = Product.objects.all()
        
        # Start as none to ensure we don't get an error
        # when loading the products page without a search term.
        query = None
        category = None
        
        # Access URL parameters by checking whether request.GET exists
        if request.GET:
            if 'categories' in request.GET:
                # Split it into a list at the commas.
                category = request.GET['categories'].split(',')
                # Use that list to filter the current query set of all products 
                # down to only products whose category name is in the list
                products = products.filter(category__name__in=category)
                # Filter a list of Category objects
                # to those passed in the URL parameter
                category = Category.objects.filter(name__in=category)
            
            # Since we named the text input in the form "q". 
            # We can just check if "q" is in request.get
            if 'q' in request.GET:
                # If "q" is a URL parameter 
                # set it equal to a variable called query.
                query = request.GET['q']
                # If the query is blank it's not going to return any results
                if not query:
                    # Use the Django messages framework 
                    # to attach an error message to the request
                    messages.error(
                        request, 
                        "You didn't enter any search criteria"
                    )
                    # Redirect back to the products URL
                    return redirect(reverse('products'))
                
                # Django can't handle basic database OR logic
                # We want to return results where the query was matched 
                # in either the product name OR the description
                # In order to accomplish this OR logic, we need to use Q
                # Set a variable equal to a Q object
                #  - Where the "name" contains the query
                #  - OR the "description" contains the query.
                # The pipe generates the OR statement.
                # The i in front of contains makes the queries case insensitive.
                queries = Q(name__icontains=query) | Q(description__icontains=query)
                products = products.filter(queries)
        
        context = {
            'products': products,
            'search_term': query,
            'current_categories': category,
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
    
    
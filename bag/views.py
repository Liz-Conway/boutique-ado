from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView

# Create your views here.
class BagContents(TemplateView):
    """ A class for rendering the bag contents page """
    template_name = 'bag/bag.html'
    
    def get(self, request):
        return render(request, self.template_name)
    

class AddToBag(TemplateView):
    """
    Add a quantity of a specified product to the shopping bag
    """
    
    def post(self, request, product_id):
        
        # Get the quantity from the form.
        # Convert it to an integer
        # since it'll come from the template as a string.
        quantity = int(request.POST.get('quantity'))
        
        # Get the redirect URL from the form so we know
        # where to redirect once the process here is finished.
        redirect_url = request.POST.get('redirectUrl')
        
        # Every request-response cycle between the server and the client,
        # (In our case between the django view on the server-side
        #  and our form making the request on the client-side.)
        #  uses a session, to allow information to be stored
        #  until the client and server are done communicating.
        # This allows us to store the contents of the shopping bag 
        # in the HTTP session,
        #  while the user browses the site and adds items to be purchased.
        # By storing the shopping bag in the session,
        # it will persist until the user closes their browser
        #  so that they can add something to the bag,
        # then browse to a different part of the site add something else
        # and so on without losing the contents of their bag.
        
        # The variable bag accesses the requests session,
        # tries to get the bag stored in the session - if it already exists,
        # and initialises it to an empty dictionary {} if it doesn't.
        # First check to see if there's a bag variable in the session,
        # and if not this code will create one
        bag = request.session.get('bag', {})
        
        if product_id in list(bag.keys()):
            # If the product is already in the bag
            # (if there's already a key in the bag dictionary
            #  matching this product id)
            # Increment its quantity
            bag[product_id] += quantity
        else:
            # This product does not exist in the shopping bag.
            # Create a key for the product in our dictionary,
            # and set its value to the quantity ordered.
            bag[product_id] = quantity
            
        # Put the bag variable into the session.
        #  Which itself is just a python dictionary.
        request.session['bag'] = bag
        
        return redirect(redirect_url)
        
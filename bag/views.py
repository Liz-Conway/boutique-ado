from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.urls.base import reverse
from django.http.response import HttpResponse
from products.models import Product
from django.contrib import messages

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
        
        product = get_object_or_404(Product, pk=product_id)
        # Get the quantity from the form.
        # Convert it to an integer
        # since it'll come from the template as a string.
        quantity = int(request.POST.get('quantity'))
        
        # Get the redirect URL from the form so we know
        # where to redirect once the process here is finished.
        redirect_url = request.POST.get('redirectUrl')
        
        size = None
        # If product size is in request.post we'll set it equal to that.
        if 'productSize' in request.POST:
            size = request.POST['productSize']
        
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
        
        if size:
            # Use a dictionary with a key of items_by_size.
            # Since we may have multiple items with this product id
            # but different sizes.
            # This allows us to structure the bags
            # so we have a single product id for each item
            # but still track multiple sizes
            if product_id in list(bag.keys()):
                # If the item is already in the bag
                
                # If another item of the same id
                # and same size already exists
                if size in bag[product_id]['products_by_size'].keys():
                    # Increment the quantity for that size
                    bag[product_id]['products_by_size'][size] += quantity
                    messages.success(
                        request,
                        f'Updated size {size.upper()} {product.name} quantity '\
                        f'to {bag[product_id]["products_by_size"][size]}'
                    )
                else:
                    # Product already exists, but this is a new size for it
                    # So set the 'product by size' to this order quantity
                    bag[product_id]['products_by_size'][size] = quantity
                    messages.success(
                        request,
                        f'Added  {product.name} (size {size.upper()}) to your bag'
                    )
            else:
                # Product is not in the bag
                # Set the 'product by size' to the order quantity
                bag[product_id] = {'products_by_size': {size: quantity}}
                messages.success(
                    request,
                    f'Added  {product.name} (size {size.upper()}) to your bag'
                )
        else:
            # No sizes so just use the product ID
            if product_id in list(bag.keys()):
                # If the product is already in the bag
                # (if there's already a key in the bag dictionary
                #  matching this product id)
                # Increment its quantity
                bag[product_id] += quantity
                messages.success(
                    request,
                    f'Updated {product.name} quantity to {bag[product_id]}'
                )
            else:
                # This product does not exist in the shopping bag.
                # Create a key for the product in our dictionary,
                # and set its value to the quantity ordered.
                bag[product_id] = quantity
                messages.success(
                    request,
                    f'Added {product.name} to your bag'
                )
            
        # Put the bag variable into the session.
        #  Which itself is just a python dictionary.
        request.session['bag'] = bag
        
        return redirect(redirect_url)
        
        
class AdjustBag(TemplateView):
    """
    Adjust the quantity of a specified product to the specified amount
    """
    
    def post(self, request, product_id):
        
        product = get_object_or_404(Product, pk=product_id)
        # Get the quantity from the form.
        # Convert it to an integer
        # since it'll come from the template as a string.
        quantity = int(request.POST.get('quantity'))
        
        # No need for a  redirect URL
        # Since we alway want to redirect back to the shopping bag page
        # redirect_url = request.POST.get('redirectUrl')
        
        size = None
        # If product size is in request.post we'll set it equal to that.
        if 'productSize' in request.POST:
            size = request.POST['productSize']
        
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
        
        # Basic idea :
        # If quantity > zero Set the product's quantity accordingly
        #  Otherwise we'll just remove the product.
        if size:
            # Use a dictionary with a key of products_by_size.
            # Since we may have multiple items with this product id
            # but different sizes.
            # This allows us to structure the bags
            # so we have a single product id for each item
            # but still track multiple sizes
            
            # Drill into the products_by_size dictionary,
            # find that specific size
            if quantity > 0:
                # Set the product's size quantity to the updated value
                bag[product_id]['products_by_size'][size] = quantity
                messages.success(
                    request,
                    f'Updated  {product.name} (size {size.upper()}) quantity '\
                    f'to {bag[product_id]["products_by_size"][size]}'
                    )
            else:
                # Remove the product's entry for the specific size
                del bag[product_id]['products_by_size'][size]
                # If updating with a quantity of zero
                # I.E., the products_by_size dictionary is now empty
                # it will evaluate to false.
                if not bag[product_id]['products_by_size']:
                    # Remove the entire product id
                    # so we don't end up with an empty products_by_size
                    # dictionary hanging around
                    bag.pop(product_id)
                messages.success(
                    request,
                    f'Removed  {product.name} (size {size.upper()}) from the bag'
                )
        else:
            # No sizes so just use the product ID
            if quantity > 0:
                # Set the product's quantity to the updated value
                bag[product_id] = quantity
                messages.success(
                    request,
                    f'Updated {product.name} quantity to {bag[product_id]}'
                )
            else:
                # Remove the product entirely by using the pop() function
                bag.pop(product_id)
                messages.success(
                    request,
                    f'Removed {product.name} from your bag'
                )
            
        # Put the bag variable into the session.
        #  Which itself is just a python dictionary.
        request.session['bag'] = bag
        
        # Redirect back to the view bag URL
        return redirect(reverse('bag'))


class RemoveFromBag(TemplateView):
    """
    Remove the item from the shopping bag
    """
    
    def post(self, request, product_id):
        
        # No need for a  redirect URL
        # Since we alway want to redirect back to the shopping bag page
        # redirect_url = request.POST.get('redirectUrl')
        
        # Wrap this entire block of code in a try block.
        try:
            product = get_object_or_404(Product, pk=product_id)
            size = None
            # If product size is in request.post we'll set it equal to that.
            if 'productSize' in request.POST:
                size = request.POST['productSize']
            
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
            # tries to get the bag stored in the session-if it already exists,
            # and initialises it to an empty dictionary {} if it doesn't.
            # First check to see if there's a bag variable in the session,
            # and if not this code will create one
            bag = request.session.get('bag', {})
            
            if size:
                # Use a dictionary with a key of products_by_size.
                # Since we may have multiple items with this product id
                # but different sizes.
                # This allows us to structure the bags
                # so we have a single product id for each item
                # but still track multiple sizes
                
                # If size is in request.POST. 
                # Delete that size key in the products_by_size dictionary
                del bag[product_id]['products_by_size'][size]
                # If that's the only size they had in the bag.
                # I.E., if the products_by_size dictionary is now empty
                # it will evaluate to false.
                if not bag[product_id]['products_by_size']:
                    # Remove the entire product id
                    # so we don't end up with an empty products_by_size 
                    # dictionary hanging around
                    bag.pop(product_id)
                messages.success(
                    request,
                    f'Removed {product.name} (size {size.upper()}) from the bag'
                )
            else:
                # There is no size
                # Removing the product is as simple as
                # popping it out of the bag
                bag.pop(product_id)
                messages.success(
                    request,
                    f'Removed {product.name} from your bag'
                )
                
            # Put the bag variable into the session.
            #  Which itself is just a python dictionary.
            request.session['bag'] = bag
            
            # Since this view will be posted to from a JavaScript function.
            # Return a 200 HTTP response.
            # Implying that the product was successfully removed
            return HttpResponse(status=200)
        # Catch any exceptions that happen
        # in order to return a 500 server error
        except Exception as ex:
            messages.error(request, f'Error removing product :  {ex}')
            return HttpResponse(status=500)
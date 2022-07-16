"""
Context processor.
Its purpose is to make this dictionary available to all templates across the entire application
Much like you can use request.user in any template
due to the presence of the built-in request context processor.
"""
from boutique_ado import settings
from decimal import Decimal
from django.shortcuts import get_object_or_404
from products.models import Product

def bag_contents(request):
    
    # An empty list for the bag items to live in
    bag_items = []
    total = 0
    product_count = 0
    
    # Retrieve the 'bag' from the session
    # or create an empty dictionary {} if it does not exist
    bag = request.session.get('bag', {})
    
    # In order to populate the values of the variables :
    # . bag_items
    # . total
    # . product_count
    # We need to iterate through all the items in the shopping bag.
    # And along the way, tally up the total cost and product count.
    # And add the products and their data to the bag items list.
    # So we can display them on the shopping bag page.
    # And elsewhere throughout the site.
    
    # First variable is the key from the bag item (we call it 'product_id')
    # Second variable is the value of that key (we are calling it 'quantity')
    for product_id, quantity in bag.items():
        # For each product id and quantity in bag.items.

        # First get the product.
        product = get_object_or_404(Product, pk=product_id)
        
        # Add quantity times the price to the total
        total += quantity * product.price
        
        # Increment the product count by the quantity.
        product_count += quantity
        
        # Add a dictionary to the list of bag items
        #  containing not only the id and the quantity,
        # but also the product object itself.
        # That will give us access to all the other fields,
        #  such as the product image and so on,
        # when iterating through the bag items in our templates.
        bag_items.append({
            'product_id': product_id,
            'quantity': quantity,
            'product': product,
        })
        
    
    # In order to entice customers to purchase more.
    # We're going to give them free delivery if they spend more than the amount
    # specified in the free delivery threshold in settings.py.
    # Check whether total is less than that threshold.
    if total < settings.FREE_DELIVERY_THRESHOLD:
        # If it is less we'll calculate delivery as 
        # the total multiplied by the standard delivery percentage
        # from settings.py. which in this case is 10%.

        # I'm also going to wrap this calculation in the decimal function
        # and import it at the top along with importing our settings file.
        # I'm using the decimal function since this is a financial transaction
        # and using float is susceptible to rounding errors.
        # So just in general using decimal is preferred when working with money
        # because it's more accurate.
        delivery = total * Decimal(
                                        settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        # Let the user know how much more they need to spend
        # to get free delivery by creating a variable called free_delivery_delta
        # This way we'll be able to entice the user across the site
        # by letting them know they can get free delivery
        # if they just buy a couple more items.
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
        
    grand_total = total + delivery
    
    
    # This context concept is the same as the context we've been using in our views
    # the only difference is we're returning it directly and making it available to
    # all templates by putting it in settings.py
    # Add all these items to the context.
    # So they'll be available in templates across the site.
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }
    
    return context;
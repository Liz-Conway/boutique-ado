from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView, View
from django.contrib import messages
from django.urls.base import reverse
from checkout.forms import OrderForm
from bag.contexts import bag_contents
from boutique_ado.settings import (
    STRIPE_PUBLIC_KEY,
    STRIPE_SECRET_KEY,
    STRIPE_CURRENCY,
)

import stripe, json
from products.models import Product
from checkout.models import OrderLineItem, Order
from boutique_ado import settings
from django.http.response import HttpResponse
from profiles.models import UserProfile
from profiles.forms import UserProfileForm


class Checkout(TemplateView):
    def get(self, request):
        stripe_public_key = STRIPE_PUBLIC_KEY
        stripe_secret_key = STRIPE_SECRET_KEY

        bag = request.session.get("bag", {})

        # Bag is empty
        if not bag:
            messages.error(request, "There's nothing in your bag")
            # This will prevent people from manually accessing the URL
            # by typing "/checkout"
            return redirect(reverse("products"))

        # Pass in the request and get the bag dictionary
        current_bag = bag_contents(request)
        # Retrieve the grand total from the current bag
        total = current_bag["grand_total"]
        # Stripe requires the amount to charge to be an integer
        stripe_total = round(total * 100)

        stripe.api_key = stripe_secret_key
        # Create the payment intent giving it the amount and the currency
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=STRIPE_CURRENCY,
        )

        # An instance of our order form - which will be empty for now.
        order_form = OrderForm()

        # Use the user's default delivery information to pre-fill the form on the checkout page.
        # Just before we create the order form in the checkout view:
        # 1.  Check whether the user is authenticated.
        # 2.  If so get their profile and use the initial parameter on the order form
        #      to pre-fill all its fields with the relevant information.
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(
                    initial={
                        # Fill in the full_name with the built in
                        # get_full_name() method on their user account.
                        "full_name": profile.user.get_full_name(),
                        # Fill in their email from their user account.
                        "email": profile.user.email,
                        # Fill everything else from the default information in their profile
                        "phone_number": profile.default_phone_number,
                        "country": profile.default_country,
                        "postcode": profile.default_postcode,
                        "town_or_city": profile.default_town_or_city,
                        "street_address1": profile.default_street_address1,
                        "street_address2": profile.default_street_address2,
                        "county": profile.default_county,
                    }
                )
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            # If the user is not authenticated => just render an empty form.
            order_form = OrderForm()

        if not stripe_public_key:
            messages.warning(
                request,
                "Stripe public key is missing.  Did you forget to set it in your environment?",
            )
        # The template
        template_name = "checkout/checkout.html"
        # Context containing the order form.
        context = {
            "order_form": order_form,
            "stripe_public_key": stripe_public_key,
            "client_secret": intent.client_secret,
        }

        return render(request, template_name, context)

    def post(self, request):
        bag = request.session.get("bag", {})

        # Doing this manually in order to skip the save info box,
        # which doesn't have a field on the order model.
        # All the other fields can come directly from the form
        form_data = {
            "full_name": request.POST["full_name"],
            "email": request.POST["email"],
            "phone_number": request.POST["phone_number"],
            "country": request.POST["country"],
            "postcode": request.POST["postcode"],
            "town_or_city": request.POST["town_or_city"],
            "street_address1": request.POST["street_address1"],
            "street_address2": request.POST["street_address2"],
            "country": request.POST["country"],
        }

        # Create an instance of the form using the form data
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            # If the form is valid --> save the order
            # but delay saving to Database until further data
            # which is in the model but not in the OrderForm is collected
            order = order_form.save(commit=False)
            # Split the "client_secret" at the word "_secret"
            # the first part of it will be the payment intent Id
            pid = request.POST.get("client_secret").split("_secret")[0]
            order.stripe_pid = pid
            # Dump the "bag" to a JSON string and set it on the order
            order.original_bag = json.dumps(bag)

            order.save()

            # Iterate through the bag items to create each line item
            # First variable is the key from the bag item (we call it 'product_id')
            # Second variable is the value of that key (we are calling it 'product_data')
            # In the case of an item with no sizes,
            # the product data will just be the quantity.
            # But in the case of a product that has sizes,
            # the product data will be a dictionary of all the products by size.
            for product_id, product_data in bag.items():
                # For each product id and quantity/data in bag.items

                try:
                    # First get the product.
                    product = Product.objects.get(id=product_id)
                    # Execute this code if the item has no sizes.
                    # Check whether or not the product data is an integer.
                    # If it's an integer -> we know the product data is just the quantity.
                    if isinstance(product_data, int):
                        # For each product ordered
                        # Create an order line item and save it
                        order_line_item = OrderLineItem(
                            order=order, product=product, quantity=product_data
                        )
                        order_line_item.save()
                    else:
                        # product data is not an integer -> Must have sizes

                        # Iterate through the each size
                        # and create a line item accordingly.
                        for size, quantity in product_data[
                            "products_by_size"
                        ].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(
                        request,
                        (
                            "One of the products in your shopping bag was not found in our database.",
                            "Please call us for assistance!",
                        ),
                    )
                    order.delete()
                    return redirect(reverse("view_bag"))

            # Attach whether or not the user wanted to save their profile information to the session
            request.session["saveInfo"] = "saveInfo" in request.POST

            # Redirect to a new page
            # passing the order number as an argument
            return redirect(
                reverse("checkoutSuccess", args=[order.order_number])
            )

        else:
            # If the order form isn't valid => attach a message letting the user know
            # and send them back to the checkout page at the bottom of this view
            # with the form errors shown
            messages.error(
                request,
                "There was an error with your form.  Please double check your information.",
            )


class CheckoutSuccess(TemplateView):
    """
    Handle successful checkouts
    """

    def get(self, request, order_number):
        # first check whether the user wanted to save their information
        # by getting that from the session
        save_info = request.session.get("saveInfo")
        # Use the order number to get the order created in the previous view
        order = get_object_or_404(Order, order_number=order_number)

        # The form has been submitted and the order has been successfully processed
        # so this is a good place to add the user profile to it

        # Skip this step for anonymous users
        # Check if the user is authenticated
        # if so they'll have a profile that was created when they created their account
        if request.user.is_authenticated:
            # Get the user's profile
            profile = UserProfile.objects.get(user=request.user)
            # Attach the user's profile to the order
            order.user_profile = profile
            order.save()

            # Save the user's info
            # Use the save info box here.
            # First determine if it was checked
            if save_info:
                # Pull the data to go in the user's profile off the order into a dictionary of profile data.
                # The dictionaries keys will match the fields on the user profile model.
                # Such as the default phone number, country, postcode, and so on
                profile_data = {
                    "default_phone_number": order.phone_number,
                    "default_country": order.country,
                    "default_postcode": order.postcode,
                    "default_town_or_city": order.town_or_city,
                    "default_street_address1": order.street_address1,
                    "default_street_address2": order.street_address2,
                    "default_county": order.county,
                }

                # Create an instance of the user profile form, using the profile data.
                # Tell it we're going to update the profile we've obtained above.
                user_profile_form = UserProfileForm(
                    profile_data, instance=profile
                )
                # If the form is valid => save it
                if user_profile_form.is_valid():
                    user_profile_form.save()

        # Success message letting the user know what their order number is
        # And that we will be sending an email to the address they put in the form
        messages.success(
            request,
            f"Order successfully processed!  Your order number is {order_number}.  A confirmation email will be sent shortly to {order.email}",
        )

        # Delete the user shopping bag from the session
        # since it'll no longer be needed
        if "bag" in request.session:
            del request.session["bag"]

        template_name = "checkout/checkoutSuccess.html"
        context = {"order": order}

        return render(request, template_name, context)


class CacheCheckoutData(View):
    """
    Determine in the webhook whether the user had the "save info" box checked.
    We can add that to the payment intent in a key called metadata,
    but we have to do it from the server-side
    because the confirm card payment method doesn't support adding it
    """

    # Before we call the confirm card payment method in the stripe JavaScript.
    # we'll make a post request to this view
    # and give it the client secret from the payment intent
    def post(self, request):
        try:
            # Split the "client_secret" at the word "_secret"
            # the first part of it will be the payment intent Id
            pid = request.POST.get("client_secret").split("_secret")[0]
            # Set up stripe with the secret key so we can modify the payment intent
            stripe.api_key = settings.STRIPE_SECRET_KEY
            # Call stripe.PaymentIntent.modify() give it the pid,
            # and tell it what we want to modify.
            # Add some metadata - add the user who's placing the order,
            # add whether or not they wanted to save their information,
            # add a JSON dump of their shopping bag (which we'll use a little later)
            stripe.PaymentIntent.modify(
                pid,
                metadata={
                    "bag": json.dumps(request.session.get("bag", {})),
                    "saveInfo": request.POST.get("save_info"),
                    "username": request.user,
                },
            )
            return HttpResponse(status=200)

        except Exception as ex:
            messages.error(
                request,
                "Sorry, your payment cannot be processed right now.  Please try again later.",
            )
            return HttpResponse(content=ex, status=400)

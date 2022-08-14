from django.template.context_processors import request
import stripe
import json
from django.http.response import HttpResponse
from .webhook_handler import StripeWH_Handler

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from boutique_ado import settings


# Will make this view require a post request and will reject get requests
@require_POST
# Stripe won't send a CSRF token like we'd normally use
@csrf_exempt
def webhook(request):
    """Listen for webhooks from Stripe"""
    print("Stripe Webhook was called")
    # Setup
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Get the webhook data and verify its signature
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        ### Stripe code ###
        # event = stripe.Event.construct_from(
        #   json.loads(payload), stripe.api_key
        # )
        ### CI code ###
        event = stripe.Webhook.construct_event(payload, sig_header, wh_secret)
    except ValueError as ve:
        # Invalid payload
        return HttpResponse(status=400)
    ### CI code ###
    except stripe.error.SignatureVerificationError as sve:
        # Invalid signature
        return HttpResponse(status=400)
    ### CI code ###
    # Generic exception handler
    except Exception as ex:
        return HttpResponse(content=ex, status=400)

    print("Webhook Success!")

    # Set up a webhook handler
    handler = StripeWH_Handler(request)

    # Map webhook events to relevant handler function
    # Dictionary keys => names of the webhooks coming from stripe.
    # Values => the actual methods inside the handler.
    event_map = {
        "payment_intent.succeeded": handler.handle_payment_intent_succeeded,
        "payment_intent.payment_failed": handler.handle_payment_intent_payment_failed,
    }

    # Get the webhook type from Stripe
    # which will be stored in a key called "type"
    # E.G.  "payment_intent.succeeded" or "payment_intent.payment failed"
    event_type = event["type"]

    # Look up the key in the dictionary.
    # And assign its value to a variable called "event_handler"
    # If there is a handler for it, get it from the event map
    event_handler = event_map.get(event_type, handler.handle_event)

    # Call the event handler with the event
    response = event_handler(event)

    return response

    ### Stripe code ###
    ### Will replace this with our own code
    # Handle the event
    # if event.type == 'payment_intent.succeeded':
    #   payment_intent = event.data.object # contains a stripe.PaymentIntent
    #   print('PaymentIntent was successful!')
    # elif event.type == 'payment_method.attached':
    #   payment_method = event.data.object # contains a stripe.PaymentMethod
    #   print('PaymentMethod was attached to a Customer!')
    # # ... handle other event types
    # else:
    #   print('Unhandled event type {}'.format(event.type))
    #
    # return HttpResponse(status=200)

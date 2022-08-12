"""
What happens if the users somehow intentionally or accidentally
closes the browser window after the payment is confirmed but before the form is submitted.
We would end up with a payment in stripe but no order in our database.
What's more, if we needed to complete
post order operations like fulfillment, sending internal email notifications and so on;
none of that stuff would be triggered because the user never fully completed their order.
This could result in a customer being charged and never receiving a confirmation email
or even worse never receiving what they ordered.
To prevent this situation we're going to build in some redundancy.
Each time an event occurs on stripe such as a payment intent being created,
a payment being completed, and so on; stripe sends out what's called a webhook we can listen for.
Webhooks are like the signals django sends each time a model is saved or deleted.
Except that they're sent securely from stripe to a URL we specify.
"""
from django.http.response import HttpResponse


class StripeWH_Handler:
    """Handle Stripe WebHooks"""

    # A setup method that's called every time an instance of the class is created
    def __init__(self, request):
        print("Stripe Webhook handler initialised")
        # Assign the request as an attribute of the class
        # just in case we need to access any attributes of the request coming from stripe
        self.request = request

    # Take the event stripe is sending us
    # and simply return an HTTP response indicating it was received.
    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        print("handle_event() called")
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}', status=200
        )

    # Sent each time a user completes the payment process
    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        print("Handling payment succeeded")
        # Once the user makes a payment, it will have our metadata attached.
        # The payment intent will be saved in a key called "event.data.object"
        intent = event.data.object

        print(f"Intent :\n {intent}")
        pid = intent.Id
        bag = intent.metadata.bag
        save_info = intent.metadata.saveInfo

        return HttpResponse(
            content=f'Webhook received: {event["type"]}', status=200
        )

    # Sent when the payment fails
    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        print("handle_payment_intent_payment_failed() called")
        return HttpResponse(
            content=f'Webhook received: {event["type"]}', status=200
        )

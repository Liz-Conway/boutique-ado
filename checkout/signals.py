# These signals are sent by django to the entire application
# after a model instance is saved and after it's deleted respectively
from django.db.models.signals import post_save, post_delete

# To receive these signals we can import receiver from django.dispatch
from django.dispatch import receiver

# Since we'll be listening for signals from the OrderLineItem model
# we'll also need that
from .models import OrderLineItem

# Special type of function which will handle signals from the post_save event
# To execute this function anytime the post_save signal is sent.
# I'll use the receiver decorator. Telling it we're receiving post_save signals
# from the OrderLineItem model
@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    Parameters :
    sender - the sender of the signal. In our case OrderLineItem
    instance - The actual instance of the model that sent it
    created - A boolean sent by django referring to
                    whether this is a new instance or one being updated
    **kwargs - Any keyword arguments
    """
    # Call order.update_total() each time a line item is attached to the order
    # Access instance.order which refers to the order
    # this specific line item is related to.
    # And call the update_total method on it
    instance.order.update_total()


# Special type of function which will
# handle signals from the post_delete event
# To execute this function anytime the post_delete signal is sent.
# Use the receiver decorator. Telling it we're receiving post_delete signals
# from the OrderLineItem model
@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    Parameters :
    sender - the sender of the signal. In our case OrderLineItem
    instance - The actual instance of the model that sent it
    **kwargs - Any keyword arguments
    """
    # Call order.update_total()
    # each time a line item attached to the order is deleted
    # Access instance.order which refers to the order
    # this specific line item is related to.
    # And call the update_total method on it
    instance.order.update_total()

from django.contrib import admin
from checkout.models import OrderLineItem, Order


class OrderLineItemAdminInline(admin.TabularInline):
    """
    Inline item allows us to add and edit line items in the admin
    right from inside the order model.
    So when we look at an order,
    we'll see a list of editable line items on the same page,
    rather than having to go to the order line item interface.
    """

    model = OrderLineItem
    # Make the line item total in the form read-only
    readonly_fields = ("lineitem_total",)


class OrderAdmin(admin.ModelAdmin):

    # Add the inlines option in the order admin class
    inlines = (OrderLineItemAdminInline,)

    # Will be calculated by our model methods.
    # Including order number, date, delivery cost, order total & grand_total
    # So we don't want anyone to have the ability to edit them
    # since it could compromise the integrity of an order.
    readonly_fields = (
        "order_number",
        "date",
        "delivery_cost",
        "order_total",
        "grand_total",
        "original_bag",
        "stripe_pid",
    )

    # Allow us to specify the order of the fields in the admin interface
    # which would otherwise be adjusted by django
    # due to the use of some read-only fields.
    # This way the order stays the same as it appears in the model.
    fields = (
        "order_number",
        "date",
        "full_name",
        "email",
        "phone_number",
        "country",
        "postcode",
        "town_or_city",
        "street_address1",
        "street_address2",
        "county",
        "delivery_cost",
        "order_total",
        "grand_total",
        "original_bag",
        "stripe_pid",
    )

    # Restrict the columns that show up in the order list
    # to only a few key items
    list_display = (
        "order_number",
        "date",
        "full_name",
        "order_total",
        "delivery_cost",
        "grand_total",
    )

    # Ordered by date in reverse chronological order
    # putting the most recent orders at the top
    ordering = ("-date",)


# Skip registering the OrderLineItem model,
# since it's accessible via the inline on the order model.
admin.site.register(Order, OrderAdmin)

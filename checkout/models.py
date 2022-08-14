import uuid  # used to generate the order number
from django.db import models
from django.db.models import Sum
from django.conf import settings
from products.models import Product
from _ast import Or


class Order(models.Model):

    # "editable=False" attribute on the order number field.
    # We're gonna automatically generate this order number.
    # And we'll want it to be unique and permanent
    # so users can find their previous orders.
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    # Use "auto_now_add" attribute on the date field
    # which will automatically set the order date and time
    # whenever a new order is created
    date = models.DateField(auto_now_add=True)

    # The last three fields will be calculated using a model method.
    # whenever an order is saved
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0
    )
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )

    # It's possible for the same customer to purchase
    # the same things twice on separate occasions
    # which would result in us finding an identical order in the database
    # when they place the second one.
    # These field ensure that each order is unique
    original_bag = models.TextField(null=False, blank=False, default="")
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default=""
    )

    # Prepended with an underscore by convention
    # to indicate it's a private method
    # which will only be used inside this class
    def _generate_order_number(self):
        """
        Generate a random, unique number using UUID
        """
        # Generate a random string of 32 characters
        # we can use as an order number
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        # Use the Sum() function across all the line-item total fields
        # for all line items on this order.
        # Use the aggregate() function
        # to add a new field to the query set called "lineitem_total_sum"
        # this field is named automatically for us.
        # We can then get the "lineitem_total__sum" and set the order total to it.
        # NB THERE IS A DOUBLE UNDERSCORE  BEFORE 'sum' where it is aggregated
        aggregation = self.lineitems.aggregate(Sum("lineitem_total"))
        line_sum = aggregation["lineitem_total__sum"]
        # Add " or 0" to the end to prevent an error
        # if we manually delete all the line items from an order
        # by making sure that this sets the order_total to zero instead of None
        self.order_total = line_sum or 0

        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            # With the order total calculated,
            # we can then calculate the delivery cost
            # using the free delivery threshold and
            # the standard delivery percentage from our settings file.
            self.delivery_cost = (
                self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
            )
        else:
            # Setting delivery cost to zero
            # if the order total is higher than the threshold.
            self.delivery_cost = 0

        # Calculate the grand total
        # Add the order total and the delivery cost together
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    # Override the default save method.
    # If the order we're saving right now doesn't have an order number.
    # We'll call the generate_order_number() method.
    # And then execute the original save() method
    def save(self, *args, **kwargs):
        """
        Override the original save() method to set the order number
        if it hasn't been set already
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()

        super().save(*args, **kwargs)

    def __str__(self):
        """
        Return the order number
        """
        return self.order_number


class OrderLineItem(models.Model):
    """
    An individual shopping bag item relating to a specific order
    And referencing the product itself, the size that was selected,
    the quantity and the total cost for that line item.
    When a user checks out:
    First use the information they put into the payment form
    to create an order instance.
    Iterate through the items in the shopping bag.
    Create an order line item for each item, attaching it to the order.
    Update the delivery cost, order total, and grand total along the way.
    """

    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="lineitems",
    )

    product = models.ForeignKey(
        Product,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    # Simple two-character char field.
    # XS, S, M, L, XL
    # Allowed to be null and blank,
    # since there are some products with no sizes
    product_size = models.CharField(max_length=2, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        blank=False,
        # Automatically calculated when the line item is saved
        editable=False,
    )

    # Override the default save method.
    # And then execute the original save() method
    def save(self, *args, **kwargs):
        """
        Override the original save() method to set the lineitem total
        and update the order total
        """
        # Multiply the product price by the quantity for each line item
        self.lineitem_total = self.product.price * self.quantity

        super().save(*args, **kwargs)

    def __str__(self):
        """
        Return the SKU of the product
        along with the order number it's part of for each order line item
        """
        return f"SKU {self.product.sku}" f" on order {self.order.order_number}"

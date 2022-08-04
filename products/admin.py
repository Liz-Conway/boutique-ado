from django.contrib import admin
from .models import Product, Category


class ProductAdmin(admin.ModelAdmin):
    # list display attribute
    # - a tuple that will tell the admin which fields to display.
    list_display = (
        "sku",
        "name",
        "category",
        "price",
        "rating",
        "image",
    )

    # Sort the products by SKU using the ordering attribute.
    # Since it's possible to sort on multiple columns note that this does
    # have to be a tuple even though it's only one field.
    # To reverse it you can simply stick a minus in front of SKU.
    # I.E. '-sku'
    ordering = ("sku",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "friendly_name",
    )


# Register the *Admin classes alongside their respective models
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)

from django import forms
from products.models import Product, Category
from products.widgets import CustomClearableFileInput


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product

        # Special dunder string called __all__ which will include all the fields
        fields = "__all__"

    # Replace the image field on the form with the custom one which utilises the widget
    image = forms.ImageField(
        label="Image", required=False, widget=CustomClearableFileInput
    )

    # Override the __init__ method to make a couple changes to the fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get all categories
        categories = Category.objects.all()
        # Create a list of tuples of the friendly names associated with their category ids.
        # This special syntax is called the list comprehension.
        # It is a shorthand way of creating a for loop that adds items to a list.
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        # Update the category field on the form
        # to use friendly names when choosing a category instead of using the id
        # The effect of this will be seen in the select box that gets generated in the form.
        # Instead of seeing the category ID or the name field we'll see the friendly name.
        self.fields["category"].choices = friendly_names

        # iterate through the rest of these fields
        for field_name, field in self.fields.items():
            # Set some classes on them to make them match the theme of the rest of our store
            field.widget.attrs["class"] = "borderBlack"

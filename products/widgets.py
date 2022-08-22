from django.forms.widgets import ClearableFileInput

# Using "as _" means we can call "gettext_lazy()" using "_()"
# It is effectively an alias.
from django.utils.translation import gettext_lazy as _


class CustomClearableFileInput(ClearableFileInput):
    """
    Inherits from Django's built in ClearableFileInput class
    """

    # Override the checkbox label with our own value
    clear_checkbox_label = _("Remove")
    # Override the initial text with our own value
    initial_text = _("Current Image")
    # Override the input text with our own value
    input_text = _("")
    # Use a custom template
    template_name = (
        "products/custom-widget-templates/custom-clearable-file-input.html"
    )

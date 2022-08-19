from django import forms
from profiles.models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # Render all fields except for the user field since that should never change
        exclude = ("user",)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on the first field
        """
        # Call the super init() method
        # to set the form up as it would be by default
        super().__init__(*args, **kwargs)
        # A dictionary of placeholders which will show up
        # in the form fields rather than having
        # clunky looking labels and empty text boxes.
        placeholders = {
            "default_phone_number": "Phone number",
            "default_postcode": "Postal Code",
            "default_town_or_city": "Town or City",
            "default_street_address1": "Street Address 1",
            "default_street_address2": "Street Address 2",
            "default_county": "County, State or Locality",
        }

        # Set the "autofocus" attribute on the default_phone_number field to True
        # so the cursor will start in the default_phone_number field
        # when the user loads the page
        self.fields["default_phone_number"].widget.attrs["autofocus"] = True

        # Iterate through the forms fields
        for field in self.fields:

            if field != "default_country":
                if self.fields[field].required:
                    # Add a star to the placeholder
                    # if it's a "required" field on the model.
                    placeholder = f"{placeholders[field]} *"
                else:
                    placeholder = placeholders[field]

                # Set all the placeholder attributes
                # to their values in the dictionary above.
                self.fields[field].widget.attrs["placeholder"] = placeholder

            # Add a CSS class we'll use later.
            self.fields[field].widget.attrs["class"] = "profileFormInput"
            # Remove the form fields' labels
            # since we won't need them given the placeholders are now set
            self.fields[field].label = False

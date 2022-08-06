# Tell django the name of the default config class for the app
# This is in "apps.py" where we imported our "signals" module
# Without this line in the "__init__.py" file, django wouldn't know about our
# custom ready() method so our signals wouldn't work.
default_app_config = "checkout.apps.CheckoutConfig"

from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "checkout"

    # To let django know that there's a
    # new signals module with some listeners in it.
    # Override the ready() method and import our signals module.
    def ready(self):
        import checkout.signals

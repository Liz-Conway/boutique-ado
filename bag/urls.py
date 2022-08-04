from django.urls import path
from bag.views import BagContents, AddToBag, AdjustBag, RemoveFromBag

urlpatterns = [
    path("", BagContents.as_view(), name="bag"),
    path("add/<product_id>", AddToBag.as_view(), name="addToBag"),
    path("adjust/<product_id>", AdjustBag.as_view(), name="adjustBag"),
    path("remove/<product_id>", RemoveFromBag.as_view(), name="removeFromBag"),
]

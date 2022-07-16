from django.urls import path
from bag.views import BagContents, AddToBag

urlpatterns = [
    path('', BagContents.as_view(), name='bag'),
    path('add/<product_id>', AddToBag.as_view(), name='add_to_bag'),
]

from django.urls import path
from home.views import HomePage
from bag.views import BagContents

urlpatterns = [
    path('', BagContents.as_view(), name='bag'),
]

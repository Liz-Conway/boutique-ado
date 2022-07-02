from django.urls import path
from home.views import HomePage

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
]

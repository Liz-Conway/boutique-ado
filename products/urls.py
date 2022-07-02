from django.urls import path
from products.views import AllProducts

urlpatterns = [
    path('', AllProducts.as_view(), name='products'),
]

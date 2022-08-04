from django.urls import path
from products.views import AllProducts, ProductDetail

urlpatterns = [
    path("", AllProducts.as_view(), name="products"),
    path("<product_id>", ProductDetail.as_view(), name="productDetails"),
]

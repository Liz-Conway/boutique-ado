from django.urls import path
from products.views import AllProducts, ProductDetail, AddProduct

urlpatterns = [
    path("", AllProducts.as_view(), name="products"),
    path("<int:product_id>/", ProductDetail.as_view(), name="productDetails"),
    path("add/", AddProduct.as_view(), name="addProduct"),
]

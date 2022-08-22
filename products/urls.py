from django.urls import path
from products.views import (
    AllProducts,
    ProductDetail,
    AddProduct,
    EditProduct,
    DeleteProduct,
)

urlpatterns = [
    path("", AllProducts.as_view(), name="products"),
    path("<int:product_id>/", ProductDetail.as_view(), name="productDetails"),
    path("add/", AddProduct.as_view(), name="addProduct"),
    path("edit/<int:product_id>/", EditProduct.as_view(), name="editProduct"),
    path(
        "delete/<int:product_id>/",
        DeleteProduct.as_view(),
        name="deleteProduct",
    ),
]

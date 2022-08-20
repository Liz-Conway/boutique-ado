from django.urls import path
from profiles.views import ProfileView, OrderHistory

urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
    path(
        "orderHistory/<order_number>",
        OrderHistory.as_view(),
        name="orderHistory",
    ),
]

from django.urls import path

from .views import (
    CanceledView,
    OrderCreateView,
    OrderDetailView,
    OrderListView,
    OrderSuccessView,
)

app_name = "orders"

urlpatterns = [
    path("create/", OrderCreateView.as_view(), name="order-create"),
    path("success/", OrderSuccessView.as_view(), name="order-success"),
    path("canceled/", CanceledView.as_view(), name="order-canceled"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("", OrderListView.as_view(), name="order-list"),
]

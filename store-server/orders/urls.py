from django.urls import path

from .views import OrderCreateView, OrderSuccessView
from .views import CanceledView

app_name = "orders"

urlpatterns = [
    path("create/", OrderCreateView.as_view(), name="order-create"),
    path("success/", OrderSuccessView.as_view(), name="order-success"),
    path("canceled/", CanceledView.as_view(), name="order-canceled"),
]

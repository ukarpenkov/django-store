from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.products, name="index"),
    path("basket/", views.basket, name="basket"),
    path("basket/add/<int:product_id>/", views.basket_add, name="basket_add"),
    path("basket/update/<int:basket_id>/", views.basket_update, name="basket_update"),
    path("basket/remove/<int:basket_id>/", views.basket_remove, name="basket_remove"),
]
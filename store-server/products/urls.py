from django.urls import path
from . import views
from .views import BasketListView, ProductsListView

app_name = "products"

urlpatterns = [
    path("", ProductsListView.as_view(), name="index"),
    path("basket/", BasketListView.as_view(), name="basket"),
    path("basket/add/<int:product_id>/", views.basket_add, name="basket_add"),
    path("basket/update/<int:basket_id>/", views.basket_update, name="basket_update"),
    path("basket/remove/<int:basket_id>/", views.basket_remove, name="basket_remove"),
    path("category/<int:category_id>/", ProductsListView.as_view(), name="category"),
    path("page/<int:page_number>/", ProductsListView.as_view(), name="page"),
]
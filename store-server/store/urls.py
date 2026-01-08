from django.contrib import admin
from django.urls import path, include
from products.views import index, products

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('products/', products, name='products'),
]

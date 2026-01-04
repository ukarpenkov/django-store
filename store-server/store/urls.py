from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Root routes (enable after creating the app and its urls.py)
    path('', include('products.urls')),
]

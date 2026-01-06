from django.contrib import admin
from django.urls import path, include
from django.views.debug import default_urlconf

urlpatterns = [
    path('', default_urlconf),
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
]

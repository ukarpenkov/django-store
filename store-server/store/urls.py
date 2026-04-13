# from store import settings
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from products.views import IndexView

from orders.views import my_webhook_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", IndexView.as_view(), name="index"),
    path("products/", include("products.urls")),
    path(
        "users/",
        include(("users.urls", "users"), namespace="users"),
    ),
    path("accounts/", include("allauth.urls")),
    path("orders/", include(("orders.urls", "orders"), namespace="orders")),
    path("webhook/stripe/", my_webhook_view, name="stripe-webhook"),
]

if settings.DEBUG:
    urlpatterns = [
        path("__debug__/", include("debug_toolbar.urls")),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

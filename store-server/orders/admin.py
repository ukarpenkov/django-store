from django.contrib import admin

from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email", "status", "created", "initiator")
    list_filter = ("status", "created")
    search_fields = ("id", "first_name", "last_name", "email", "initiator__username")
    readonly_fields = ("created",)

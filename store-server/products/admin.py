from django.contrib import admin
from .models import Product, ProductCategory


class ProductCategoryAdmin(admin.ModelAdmin):
    ordering = ['name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity', 'category']
    list_filter = ['category']
    list_editable = ['price', 'quantity']
    search_fields = ['name', 'description']
    ordering = ['name']
    list_per_page = 10


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)

from django.contrib import admin

from products.admin import BasketAdmin
from .models import User, EmailVerification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    inlines = (BasketAdmin,)
    extra = 0


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'created', 'expiration')
    list_filter = ('created',)
    search_fields = ('user__email', 'code')

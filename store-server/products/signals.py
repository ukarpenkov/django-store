from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Product
from .product_list_cache import bump_product_list_cache


@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def invalidate_product_list_cache(**kwargs) -> None:
    bump_product_list_cache()

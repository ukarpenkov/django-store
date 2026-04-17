from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.db import models
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def _price_to_stripe_unit_amount(price) -> int:
    minor = (price * Decimal("100")).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP
    )
    return int(minor)

class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    image = models.ImageField(
        upload_to="product_images/", null=True, blank=True
    )
    category = models.ForeignKey(
        ProductCategory,
        related_name="products",
        on_delete=models.CASCADE,
    )
    stripe_product_id = models.CharField(max_length=100, null=True, blank=True)
    stripe_product_price_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        old = None
        if self.pk:
            old = (
                Product.objects.filter(pk=self.pk)
                .values(
                    "name",
                    "description",
                    "price",
                    "stripe_product_id",
                    "stripe_product_price_id",
                )
                .first()
            )
        super().save(*args, **kwargs)

        stripe_field_updates = {}
        if not self.stripe_product_id:
            product = stripe.Product.create(
                name=self.name,
                description=self.description or "",
            )
            price = stripe.Price.create(
                product=product.id,
                unit_amount=_price_to_stripe_unit_amount(self.price),
                currency="rub",
            )
            stripe_field_updates["stripe_product_id"] = product.id
            stripe_field_updates["stripe_product_price_id"] = price.id
        elif old:
            desc_old = old.get("description") or ""
            desc_new = self.description or ""
            if old["name"] != self.name or desc_old != desc_new:
                stripe.Product.modify(
                    self.stripe_product_id,
                    name=self.name,
                    description=desc_new,
                )
            if old["price"] != self.price:
                price = stripe.Price.create(
                    product=self.stripe_product_id,
                    unit_amount=_price_to_stripe_unit_amount(self.price),
                    currency="rub",
                )
                stripe_field_updates["stripe_product_price_id"] = price.id

        if stripe_field_updates:
            Product.objects.filter(pk=self.pk).update(**stripe_field_updates)
            for key, value in stripe_field_updates.items():
                setattr(self, key, value)

    def create_stripe_product_price(self):
        """Создаёт Product и Price в Stripe (идентификаторы сохраняются при следующем save())."""
        product = stripe.Product.create(
            name=self.name,
            description=self.description or "",
        )
        price = stripe.Price.create(
            product=product.id,
            unit_amount=_price_to_stripe_unit_amount(self.price),
            currency="rub",
        )
        return product.id, price.id


class Basket(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Корзина для {self.user.username} | "
            f"Продукт {self.product.name}"
        )

    @property
    def sum(self):
        return self.quantity * self.product.price

from decimal import Decimal

from django.db import models
from users.models import User

class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, "Создан"),
        (PAID, "Оплачен"),
        (ON_WAY, "В пути"),
        (DELIVERED, "Доставлен"),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=100)
    basket_history = models.JSONField(default=dict)
    status = models.SmallIntegerField(choices=STATUSES, default=CREATED)
    created = models.DateTimeField(auto_now_add=True)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    @property
    def total_sum(self) -> Decimal:
        total = Decimal("0")
        for entry in (self.basket_history or {}).values():
            raw = entry.get("sum")
            if raw is not None:
                total += Decimal(str(raw))
        return total

    def __str__(self):
        return f"Order {self.id} by {self.initiator.username}"
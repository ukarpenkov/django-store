from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from orders.models import Order
from orders.views import fulfill_checkout
from products.models import Basket, Product, ProductCategory
from users.models import User


class StripeCheckoutFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="buyer",
            password="secret123",
            email="buyer@example.com",
        )
        self.other_user = User.objects.create_user(
            username="other",
            password="secret123",
            email="other@example.com",
        )
        self.category = ProductCategory.objects.create(
            name="Тестовая категория",
            description="Для тестов заказа",
        )
        self.product = Product.objects.create(
            name="Тестовый товар",
            description="Описание",
            price=Decimal("99.99"),
            quantity=100,
            category=self.category,
            stripe_product_id="prod_test_1",
            stripe_product_price_id="price_test_1",
        )

    @patch("orders.views.stripe.checkout.Session.create")
    def test_create_order_keeps_basket_until_payment_confirmed(self, mocked_create):
        mocked_create.return_value = SimpleNamespace(url="https://checkout.stripe.test")

        basket = Basket.objects.create(
            user=self.user,
            product=self.product,
            quantity=2,
        )
        self.client.login(username="buyer", password="secret123")

        response = self.client.post(
            reverse("orders:order-create"),
            data={
                "first_name": "Ivan",
                "last_name": "Ivanov",
                "email": "buyer@example.com",
                "address": "Moscow",
            },
        )

        self.assertEqual(response.status_code, 303)
        self.assertEqual(Basket.objects.filter(pk=basket.pk).count(), 1)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.first().status, Order.CREATED)

    @patch("orders.views.stripe.checkout.Session.retrieve")
    def test_fulfill_checkout_marks_paid_and_clears_purchased_basket(self, mocked_retrieve):
        purchased = Basket.objects.create(
            user=self.user,
            product=self.product,
            quantity=1,
        )
        should_stay_same_user = Basket.objects.create(
            user=self.user,
            product=self.product,
            quantity=3,
        )
        should_stay_other_user = Basket.objects.create(
            user=self.other_user,
            product=self.product,
            quantity=4,
        )

        order = Order.objects.create(
            first_name="Ivan",
            last_name="Ivanov",
            email="buyer@example.com",
            address="Moscow",
            basket_history={
                str(purchased.id): {
                    "product_name": self.product.name,
                    "quantity": purchased.quantity,
                    "price": str(self.product.price),
                    "sum": str(purchased.sum),
                }
            },
            initiator=self.user,
        )

        mocked_retrieve.return_value = {"client_reference_id": str(order.id)}
        fulfill_checkout("cs_test_123")

        order.refresh_from_db()
        self.assertEqual(order.status, Order.PAID)
        self.assertFalse(Basket.objects.filter(pk=purchased.pk).exists())
        self.assertTrue(Basket.objects.filter(pk=should_stay_same_user.pk).exists())
        self.assertTrue(Basket.objects.filter(pk=should_stay_other_user.pk).exists())

import stripe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from orders.form import OrderForm
from orders.models import Order
from products.models import Basket
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class OrderCreateView(LoginRequiredMixin, FormView):
    template_name = "orders/order-create.html"
    form_class = OrderForm
    success_url = reverse_lazy("orders:order-success")
    title = "Store - Оформление заказа"


    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        success_url = f"{settings.SITE_URL}{reverse_lazy('orders:order-success')}"
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, price_1234) of the product you want to sell
                    "price": "{{PRICE_ID}}",
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=success_url,
        )


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        basket_items = list(
            Basket.objects.filter(user=self.request.user)
            .select_related("product")
            .order_by("-created_timestamp")
        )
        context["basket"] = basket_items
        context["basket_total_sum"] = sum((item.sum for item in basket_items), 0)
        context["basket_total_quantity"] = sum(
            (item.quantity for item in basket_items), 0
        )
        context["title"] = "Store - Оформление заказа"
        return context

    def form_valid(self, form):
        basket_qs = Basket.objects.filter(user=self.request.user).select_related(
            "product"
        )
        if not basket_qs.exists():
            form.add_error(None, "Корзина пуста. Добавьте товары и попробуйте снова.")
            return self.form_invalid(form)

        basket_history = {
            str(item.id): {
                "product_name": item.product.name,
                "quantity": item.quantity,
                "price": str(item.product.price),
                "sum": str(item.sum),
            }
            for item in basket_qs
        }
        Order.objects.create(
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            email=form.cleaned_data["email"],
            address=form.cleaned_data["address"],
            basket_history=basket_history,
            initiator=self.request.user,
        )
        basket_qs.delete()
        return super().form_valid(form)


class OrderSuccessView(TemplateView):
    template_name = "orders/success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Store - Спасибо за заказ!"
        return context

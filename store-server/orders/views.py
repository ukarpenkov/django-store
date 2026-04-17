from decimal import Decimal, ROUND_HALF_UP

import stripe
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView


from django.views.decorators.csrf import csrf_exempt

client = stripe.StripeClient(settings.STRIPE_SECRET_KEY)
endpoint_secret = settings.STRIPE_ENDPOINT_SECRET   

from django.http import HttpResponse


from orders.form import OrderForm
from orders.models import Order
from products.models import Basket

stripe.api_key = settings.STRIPE_SECRET_KEY

class OrderCreateView(LoginRequiredMixin, FormView):
    template_name = "orders/order-create.html"
    form_class = OrderForm
    success_url = reverse_lazy("orders:order-success")
    title = "Store - Оформление заказа"

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

        line_items = []
        for item in basket_qs:
            unit_minor = (item.product.price * Decimal("100")).quantize(
                Decimal("1"), rounding=ROUND_HALF_UP
            )
            line_items.append(
                {
                    "price_data": {
                        "currency": "rub",
                        "product_data": {"name": item.product.name},
                        "unit_amount": int(unit_minor),
                    },
                    "quantity": item.quantity,
                }
            )

        order = Order.objects.create(
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            email=form.cleaned_data["email"],
            address=form.cleaned_data["address"],
            basket_history=basket_history,
            initiator=self.request.user,
        )

        base = settings.SITE_URL.rstrip("/")
        success_path = reverse("orders:order-success")
        cancel_path = reverse("orders:order-canceled")
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode="payment",
            success_url=f"{base}{success_path}?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{base}{cancel_path}",
            client_reference_id=str(order.id),
        )

        return HttpResponseRedirect(checkout_session.url, status=303)


class OrderSuccessView(TemplateView):
    template_name = "orders/success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Store - Спасибо за заказ!"
        return context


class CanceledView(TemplateView):
    template_name = "orders/canceled.html"


def fulfill_checkout(session_id: str) -> None:
    session = stripe.checkout.Session.retrieve(session_id)
    ref = session.get("client_reference_id")
    if not ref:
        return
    try:
        order_pk = int(ref)
    except (TypeError, ValueError):
        return
    order = Order.objects.filter(pk=order_pk).select_related("initiator").first()
    if not order:
        return

    updated = Order.objects.filter(pk=order_pk, status=Order.CREATED).update(
        status=Order.PAID
    )
    if not updated:
        return

    purchased_basket_ids = []
    for basket_id in order.basket_history.keys():
        try:
            purchased_basket_ids.append(int(basket_id))
        except (TypeError, ValueError):
            continue

    if purchased_basket_ids:
        Basket.objects.filter(
            user=order.initiator, id__in=purchased_basket_ids
        ).delete()


@csrf_exempt
def my_webhook_view(request):
  payload = request.body

  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = client.construct_event(
      payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  if (
    event['type'] == 'checkout.session.completed'
    or event['type'] == 'checkout.session.async_payment_succeeded'
  ):
    fulfill_checkout(event['data']['object']['id'])

  return HttpResponse(status=200)


from django.views.generic import TemplateView


class OrderCreateView(TemplateView):
    template_name = "orders/order-create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Store - Оформление заказа"
        return context


class OrderSuccessView(TemplateView):
    template_name = "orders/success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Store - Спасибо за заказ!"
        return context

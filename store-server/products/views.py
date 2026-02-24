from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView

from .models import Basket, Product, ProductCategory


class IndexView(TemplateView):
    template_name = "products/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Store"
        return context


def products(request, category_id=None, page_number=1):
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    page_number = request.GET.get("page", page_number)
    paginator = Paginator(products, 3)
    page = paginator.get_page(page_number)
    context = {
        "title": "Store - Каталог",
        "products": page.object_list,
        "page": page,
        "categories": ProductCategory.objects.all(),
    }
    return render(request, "products/products.html", context)


@login_required
def basket(request):
    basket_items = (
        Basket.objects.filter(user=request.user)
        .select_related("product")
        .order_by("-created_timestamp")
    )
    context = {
        "title": "Store - Корзина",
        "basket": basket_items,
        "basket_total_sum": sum((item.sum for item in basket_items), 0),
        "basket_total_quantity": sum((item.quantity for item in basket_items), 0),
    }
    return render(request, "products/basket_page.html", context)


@login_required
def basket_add(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if not product:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

    quantity_raw = request.POST.get("quantity", 1)
    try:
        quantity_to_add = int(quantity_raw)
    except (TypeError, ValueError):
        quantity_to_add = 1

    quantity_to_add = max(1, quantity_to_add)
    quantity_to_add = min(quantity_to_add, product.quantity)

    if quantity_to_add <= 0:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

    basket_item, _ = Basket.objects.get_or_create(
        user=request.user, product=product, defaults={"quantity": 0}
    )
    basket_item.quantity = min(basket_item.quantity + quantity_to_add, product.quantity)
    basket_item.save(update_fields=["quantity"])

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def basket_update(request, basket_id):
    if request.method != "POST":
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

    basket_item = get_object_or_404(Basket, id=basket_id, user=request.user)

    quantity_raw = request.POST.get("quantity", 1)
    try:
        quantity = int(quantity_raw)
    except (TypeError, ValueError):
        quantity = basket_item.quantity

    if quantity <= 0:
        basket_item.delete()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

    quantity = min(quantity, basket_item.product.quantity)
    basket_item.quantity = quantity
    basket_item.save(update_fields=["quantity"])

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def basket_remove(request, basket_id):
    if request.method == "POST":
        basket_item = Basket.objects.filter(id=basket_id, user=request.user).first()
        if basket_item:
            basket_item.delete()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

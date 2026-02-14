from statistics import quantiles
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Basket, Product, ProductCategory


def index(request):
    context = {"title": "Store"}
    return render(request, "products/index.html", context)


def products(request):
    context = {
        "title": "Store - Каталог",
        "products": Product.objects.all(),
        "categories": ProductCategory.objects.all(),
    }
    return render(request, "products/products.html", context)


def basket_add(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

    basket, created = Basket.objects.get_or_create(
        user=request.user, product=product, defaults={"quantity": 1}
    )

    if not created:
        from django.db.models import F

        Basket.objects.filter(user=request.user, product=product).update(
            quantity=F("quantity") + 1
        )

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

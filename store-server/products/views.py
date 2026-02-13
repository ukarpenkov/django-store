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
    product = Product.objects.get(id = product_id)
    basket = Basket.objects.filter(user=request.user, product=product)

    if not basket.exists():
        Basket.objects.create(user=request.user, product=product, quantity = 1)
    else:
        basket = basket.first()
        basket.quantity +=1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
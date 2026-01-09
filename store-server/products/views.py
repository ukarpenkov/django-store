from django.shortcuts import render


def index(request):
    context = {"title": "Store", "username": "Valeriia", "is_promoted": True}
    return render(request, "products/index.html", context)


def products(request):
    return render(request, "products/products.html")

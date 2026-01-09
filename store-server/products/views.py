from django.shortcuts import render


def index(request):
    context = {"title": "Store"}
    return render(request, "products/index.html", context)


def products(request):
    context = {
        "title": "Store - Каталог",
        "products": [
            {
                "name": "Худи черного цвета с монограммами adidas Originals",
                "price": 6090,
                "image_url": "/vendor/img/products/Adidas-hoodie.png",
                "description": "Черное худи с монограммами adidas Originals, выполненное из мягкого хлопкового флиса. Модель с капюшоном и длинными рукавами оформлена фирменными 3 полосками на рукавах и крупным логотипом Trefoil спереди.",
            },
            {
                "name": "Синяя куртка The North Face",
                "price": 23725,
                "image_url": "/vendor/img/products/Blue-jacket-The-North-Face.png",
                "description": "Синяя куртка The North Face из прочного материала с водоотталкивающей пропиткой. Модель с капюшоном, застежкой на молнию и эластичными манжетами защитит вас от ветра и дождя во время прогулок по городу и активного отдыха на природе.",
            },
            {
                "name": "Коричневый спортивный oversized-топ ASOS DESIGN",
                "price": 3390,
                "image_url": "/vendor/img/products/Brown-sports-oversized-top-ASOS-DESIGN.png",
                "description": "Коричневый спортивный oversized-топ ASOS DESIGN из мягкого хлопкового джерси. Модель с круглым вырезом и короткими рукавами оформлена контрастной отделкой и логотипом ASOS DESIGN на груди.",
            },
        ],
    }
    return render(request, "products/products.html", context)

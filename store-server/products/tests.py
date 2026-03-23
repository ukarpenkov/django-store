from django.test import TestCase, Client
from django.urls import reverse
from django.views.generic import TemplateView

from .models import Product, ProductCategory


class IndexViewTestCase(TestCase):
    """Тесты для IndexView"""

    def setUp(self):
        """Инициализация тестового клиента"""
        self.client = Client()

    def test_index_view_uses_correct_template(self):
        """Проверяет, что IndexView использует правильный шаблон"""
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, "products/index.html")

    def test_index_view_has_correct_title_in_context(self):
        """Проверяет, что title в контексте равен 'Store'"""
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Store")

    def test_index_view_context_data_method(self):
        """Проверяет метод get_context_data напрямую"""
        from products.views import IndexView

        view = IndexView()
        context = view.get_context_data()
        self.assertIn("title", context)
        self.assertEqual(context["title"], "Store")

    def test_index_view_status_code(self):
        """Проверяет, что view возвращает статус 200"""
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)


class ProductsViewTestCase(TestCase):
    """Тесты для ProductsListView"""

    def setUp(self):
        """Инициализация тестового клиента и тестовых данных"""
        self.client = Client()

        # Создаем дополнительные категории для тестирования (кроме тех что в миграции)
        self.test_category1 = ProductCategory.objects.create(
            name="Электроника", description="Электронные товары"
        )
        self.test_category2 = ProductCategory.objects.create(
            name="Книги", description="Книги и учебники"
        )

        # Создаем товары для тестовой категории 1
        self.test_product1 = Product.objects.create(
            name="Ноутбук",
            description="Мощный ноутбук",
            price=999.99,
            quantity=5,
            category=self.test_category1,
        )
        self.test_product2 = Product.objects.create(
            name="Монитор",
            description="4K монитор",
            price=399.99,
            quantity=10,
            category=self.test_category1,
        )
        self.test_product3 = Product.objects.create(
            name="Клавиатура",
            description="Механическая клавиатура",
            price=149.99,
            quantity=15,
            category=self.test_category1,
        )

        # Создаем товары для тестовой категории 2
        self.test_product4 = Product.objects.create(
            name="Python для начинающих",
            description="Учебник по Python",
            price=29.99,
            quantity=20,
            category=self.test_category2,
        )
        self.test_product5 = Product.objects.create(
            name="Django книга",
            description="Полное руководство Django",
            price=39.99,
            quantity=12,
            category=self.test_category2,
        )

    def test_products_view_status_code(self):
        """Проверяет, что view возвращает статус 200"""
        response = self.client.get(reverse("products:index"))
        self.assertEqual(response.status_code, 200)

    def test_products_view_uses_correct_template(self):
        """Проверяет, что используется правильный шаблон"""
        response = self.client.get(reverse("products:index"))
        self.assertTemplateUsed(response, "products/products.html")

    def test_products_view_displays_all_products(self):
        """Проверяет, что на странице отображаются товары (с пагинацией)"""
        response = self.client.get(reverse("products:index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("object_list", response.context)
        # Так как paginate_by = 3, на первой странице будут первые 3 товара
        products = response.context["object_list"]
        self.assertEqual(len(products), 3)
        # Проверяем, что всего товаров больше 5 (7 из миграции + 5 созданных = 12)
        self.assertGreater(Product.objects.count(), 5)

    def test_products_view_has_correct_title(self):
        """Проверяет, что title в контексте правильный"""
        response = self.client.get(reverse("products:index"))
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Store - Каталог")

    def test_products_view_has_categories_in_context(self):
        """Проверяет, что категории присутствуют в контексте"""
        response = self.client.get(reverse("products:index"))
        self.assertIn("categories", response.context)
        categories = response.context["categories"]
        # В миграции 3 категории (Одежда, Обувь, Аксессуары), плюс 2 тестовые
        self.assertEqual(categories.count(), 5)
        self.assertIn(self.test_category1, categories)
        self.assertIn(self.test_category2, categories)

    def test_products_view_filter_by_category(self):
        """Проверяет отображение товаров определённой категории"""
        # Переходим на страницу категории 1 (Электроника)
        url = reverse(
            "products:category", kwargs={"category_id": self.test_category1.id}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")

        # Проверяем, что отображаются только товары категории 1
        products = response.context["object_list"]
        self.assertEqual(len(products), 3)  # Все товары категории 1 (paginate_by = 3)

        for product in products:
            self.assertEqual(product.category.id, self.test_category1.id)

    def test_products_view_filter_by_different_category(self):
        """Проверяет отображение товаров другой категории"""
        # Переходим на страницу категории 2 (Книги)
        url = reverse(
            "products:category", kwargs={"category_id": self.test_category2.id}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        # Проверяем, что отображаются только товары категории 2
        products = response.context["object_list"]
        self.assertEqual(len(products), 2)  # 2 товара в категории 2

        for product in products:
            self.assertEqual(product.category.id, self.test_category2.id)
            self.assertIn(product, [self.test_product4, self.test_product5])

    def test_products_view_pagination(self):
        """Проверяет пагинацию товаров"""
        # На первой странице должно быть 3 товара
        response = self.client.get(reverse("products:index"))
        self.assertEqual(len(response.context["object_list"]), 3)

        # Переходим на вторую страницу
        response = self.client.get(reverse("products:index") + "?page=2")
        self.assertEqual(response.status_code, 200)
        # На второй странице должно быть 3 товара (всего 12)
        self.assertEqual(len(response.context["object_list"]), 3)

        # Переходим на третью страницу
        response = self.client.get(reverse("products:index") + "?page=3")
        self.assertEqual(response.status_code, 200)
        # На третьей странице должно быть 3 товара
        self.assertEqual(len(response.context["object_list"]), 3)

        # Переходим на четвёртую страницу
        response = self.client.get(reverse("products:index") + "?page=4")
        self.assertEqual(response.status_code, 200)
        # На четвёртой странице должно быть 3 товара
        self.assertEqual(len(response.context["object_list"]), 3)

    def test_products_view_category_with_pagination(self):
        """Проверяет пагинацию товаров в категории"""
        # На странице категории 1 (у которой 3 товара)
        url = reverse(
            "products:category", kwargs={"category_id": self.test_category1.id}
        )
        response = self.client.get(url)

        # Все товары помещаются на одной странице
        self.assertEqual(len(response.context["object_list"]), 3)

        # Попытка перейти на вторую страницу для этой категории
        # Django возвращает 404 для пустых страниц, если allow_empty_first_page=True (по умолчанию)
        response = self.client.get(url + "?page=2")
        # На второй странице товаров нет, поэтому получаем 404
        self.assertEqual(response.status_code, 404)

    def test_products_view_invalid_category(self):
        """Проверяет отображение при несуществующей категории"""
        # Пытаемся получить товары несуществующей категории
        url = reverse("products:category", kwargs={"category_id": 9999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        # Список товаров должен быть пустым
        self.assertEqual(len(response.context["object_list"]), 0)

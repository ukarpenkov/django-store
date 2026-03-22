from django.test import TestCase, Client
from django.urls import reverse
from django.views.generic import TemplateView


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

from django.contrib.messages import get_messages
from django.core import mail
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from users.models import EmailVerification, User


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    # Иначе auth.login() падает: несколько бэкендов (allauth + ModelBackend)
    AUTHENTICATION_BACKENDS=[
        "django.contrib.auth.backends.ModelBackend",
    ],
)
class UserRegistrationViewTestCase(TestCase):
    """Тесты для UserRegistrationView"""

    def setUp(self):
        self.client = Client()
        self.url = reverse("users:register")
        self.valid_payload = {
            "username": "new_register_user",
            "email": "newuser@example.com",
            "first_name": "Иван",
            "last_name": "Тестов",
            "password1": "StrongUniquePass9!",
            "password2": "StrongUniquePass9!",
        }

    def test_register_get_status_and_template(self):
        """GET: страница регистрации отдаётся с нужным шаблоном"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")

    def test_register_get_shows_empty_form(self):
        """GET: в контексте есть форма регистрации"""
        response = self.client.get(self.url)
        self.assertIn("form", response.context)
        self.assertFalse(response.context["form"].is_bound)

    def test_register_post_valid_creates_user_redirects_and_logs_in(self):
        """POST с валидными данными: пользователь создан, редирект на логин, сессия"""
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertRedirects(response, reverse("users:login"), fetch_redirect_response=False)

        user = User.objects.get(username=self.valid_payload["username"])
        self.assertEqual(user.email, self.valid_payload["email"])
        self.assertEqual(user.first_name, self.valid_payload["first_name"])
        self.assertEqual(user.last_name, self.valid_payload["last_name"])

        self.assertEqual(
            int(self.client.session["_auth_user_id"]),
            user.pk,
        )

        self.assertTrue(
            EmailVerification.objects.filter(user=user).exists(),
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.valid_payload["email"], mail.outbox[0].to)

    def test_register_post_valid_success_message_after_follow(self):
        """После успешной регистрации показывается success-сообщение"""
        response = self.client.post(self.url, data=self.valid_payload, follow=True)
        self.assertEqual(response.status_code, 200)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Вы успешно зарегистрировались!", messages)

    def test_register_post_password_mismatch_returns_200_with_errors(self):
        """Несовпадение паролей: форма с ошибками, пользователь не создаётся"""
        data = {**self.valid_payload, "password2": "OtherPass9!"}
        before = User.objects.count()
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")
        self.assertFalse(response.context["form"].is_valid())
        self.assertEqual(User.objects.count(), before)

    def test_register_post_duplicate_username(self):
        """Повторный username: ошибка формы, второй пользователь не создаётся"""
        User.objects.create_user(
            username=self.valid_payload["username"],
            email="existing@example.com",
            password="ExistingPass9!",
        )
        before = User.objects.count()
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["form"].is_valid())
        self.assertIn("username", response.context["form"].errors)
        self.assertEqual(User.objects.count(), before)

    def test_register_post_invalid_email(self):
        """Некорректный email: 200 и ошибка поля email"""
        data = {**self.valid_payload, "email": "not-an-email"}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["form"].is_valid())
        self.assertIn("email", response.context["form"].errors)

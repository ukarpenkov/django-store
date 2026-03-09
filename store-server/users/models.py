from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


class User(AbstractUser):
    image = models.ImageField(upload_to="user_images/", null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True,
        help_text="The groups this user belongs to.",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_set",
        blank=True,
        help_text="Specific permissions for this user.",
    )

    class Meta:
        db_table = "auth_user"


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f"EmailVerification object for {self.user.email}"

    def send_verification_email(self):
        link = reverse("users:verify", kwargs={"code": str(self.code)})
        verification_url = f"{getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')}{link}"
        send_mail(
            subject="Email verification",
            message=f"Follow the link to verify your email: {verification_url}",
            from_email=settings.DEFAULT_FROM_EMAIL or "noreply@store.com",
            recipient_list=[self.user.email],
            fail_silently=False,
        )
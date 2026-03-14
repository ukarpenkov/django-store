from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path(
        "verify/<str:email>/<str:code>/",
        views.EmailVerificationView.as_view(),
        name="verify",
    ),
]

from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("logout/", views.logout, name="logout"),
]

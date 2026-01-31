from django.shortcuts import render
from users.forms import UserLoginForm


def login(request):
    form = UserLoginForm()
    return render(request, "users/login.html", {"form": form})


def register(request):
    return render(request, "users/register.html")


def profile(request):
    return render(request, "users/profile.html")

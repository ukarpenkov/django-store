from django.shortcuts import render
from users.forms import UserLoginForm

from django.contrib import auth


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                # Redirect or process the login
            pass
    else:
        form = UserLoginForm()
    return render(request, "users/login.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            # Process the registration
            pass
    form = UserRegistrationForm()
    return render(request, "users/register.html", {"form": form})


def profile(request):
    if request.method == "POST":
        form = UserProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # Redirect or process the profile update
            pass
    form = UserProfileForm(instance=request.user)
    return render(request, "users/profile.html", {"form": form})

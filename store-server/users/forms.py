from django.contrib.auth.forms import AuthenticationForm
from users.models import User
from django import forms


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control py-4", "placeholder": "Enter your username"}
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control py-4", "placeholder": "Enter your password"}
        ),
    )

    class Meta:
        model = User
        fields = ["username", "password"]

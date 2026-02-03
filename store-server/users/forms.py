from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordChangeForm,
    UserChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
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


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control py-4", "placeholder": "Enter your username"}
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control py-4", "placeholder": "Enter your email"}
        ),
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control py-4", "placeholder": "Enter your first name"}
        ),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control py-4", "placeholder": "Enter your last name"}
        ),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control py-4", "placeholder": "Enter your password"}
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control py-4", "placeholder": "Confirm your password"}
        ),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control py-4", "readonly": True}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control py-4", "readonly": True}),
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control py-4"}),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control py-4"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

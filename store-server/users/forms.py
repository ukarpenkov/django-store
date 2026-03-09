from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordChangeForm,
    UserChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from users.models import EmailVerification, User
from django import forms
from django.utils import timezone
from datetime import timedelta
import uuid


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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            verification = EmailVerification.objects.create(
                code=uuid.uuid4(),
                user=user,
                expiration=timezone.now() + timedelta(hours=48),
            )
            verification.send_verification_email()
        return user


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
    image = forms.ImageField(
        label="Profile Image",
        required=False,
        widget=forms.ClearableFileInput(
            attrs={"class": "custom-file-input", "id": "userAvatar"}
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "image"]

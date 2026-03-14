from urllib.parse import unquote

from django.shortcuts import HttpResponseRedirect
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.urls import reverse
from users.utils import get_users_url
from django.contrib import auth

from django.utils import timezone
from products.models import Basket
from users.models import User, EmailVerification


class UserLoginView(SuccessMessageMixin, LoginView):
    authentication_form = UserLoginForm
    template_name = "users/login.html"
    redirect_authenticated_user = False
    success_message = "Вы авторизованы"


class UserRegistrationView(SuccessMessageMixin, FormView):
    form_class = UserRegistrationForm
    template_name = "users/register.html"
    success_url = get_users_url("login")
    success_message = "Вы успешно зарегистрировались!"

    def form_valid(self, form):
        form.save()
        auth.login(self.request, form.instance)
        return super().form_valid(form)


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "users/profile.html"
    success_url = get_users_url("profile")
    login_url = get_users_url("login")

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        basket_items = (
            Basket.objects.filter(user=self.request.user)
            .select_related("product")
            .order_by("-created_timestamp")
        )
        context["basket"] = basket_items
        context["basket_total_sum"] = sum(
            (item.sum for item in basket_items), 0
        )
        context["basket_total_quantity"] = sum(
            (item.quantity for item in basket_items), 0
        )
        return context


class EmailVerificationView(TemplateView):
    template_name = "users/email_verification.html"
    title = "Store - Подтверждение электронной почты"

    def get(self, request, *args, **kwargs):
        email = unquote(kwargs.get("email", ""))
        code = kwargs.get("code")
        verification = EmailVerification.objects.filter(
            code=code, user__email=email
        ).first()
        if verification and verification.expiration > timezone.now():
            verification.user.is_verified_email = True
            verification.user.save()
            verification.delete()
            context = self.get_context_data()
            context["title"] = self.title
            return self.render_to_response(context)
        return HttpResponseRedirect(get_users_url("register"))


class UserLogoutView(LoginRequiredMixin, View):
    login_url = get_users_url("login")

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return HttpResponseRedirect(reverse("index"))

    def post(self, request, *args, **kwargs):
        auth.logout(request)
        return HttpResponseRedirect(reverse("index"))

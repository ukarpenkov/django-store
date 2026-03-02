from django.shortcuts import render, HttpResponseRedirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.urls import reverse, reverse_lazy
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from products.models import Basket
from users.models import User


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                next_url = request.POST.get("next") or request.GET.get("next", reverse("index"))
                if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts=request.get_host()):
                    return HttpResponseRedirect(next_url)
                return HttpResponseRedirect(reverse("index"))
            pass
    else:
        form = UserLoginForm()
    context = {"form": form, "next": request.GET.get("next", "")}
    return render(request, "users/login.html", context)


class UserRegistrationView(FormView):
    form_class = UserRegistrationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Вы успешно зарегистрировались!")
        auth.login(self.request, form.instance)
        return HttpResponseRedirect(reverse("users:login"))


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")
    login_url = reverse_lazy("users:login")

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
        context["basket_total_sum"] = sum((item.sum for item in basket_items), 0)
        context["basket_total_quantity"] = sum((item.quantity for item in basket_items), 0)
        return context


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("index"))
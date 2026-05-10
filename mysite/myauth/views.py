from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.utils.translation import gettext_lazy as _, ngettext

from .models import Profile, User
from .forms import ProfileAvatarForm


class HelloView(View):
    welcome_messages = _("welcome hello world!")

    def get(self, request: HttpRequest) -> HttpResponse:
        items_str = request.GET.get("items") or 0
        items = int(items_str)
        products_line = ngettext(
            "one product",
            "{count} products",
            items
        )
        products_line = products_line.format(count=items)
        return HttpResponse(
            f"<h1>{self.welcome_messages}</h1>"
            f"<h2>{products_line}</h2>"
        )


class UsersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "myauth/users_list.html"
    context_object_name = "users"

    def get_queryset(self):
        return User.objects.select_related('profile').all()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "myauth/user_detail.html"
    context_object_name = "user_detail"

    def get_object(self, queryset=None):
        return get_object_or_404(
            User.objects.select_related('profile'),
            pk=self.kwargs.get('pk')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_to_show = self.get_object()
        context['can_edit'] = (
                self.request.user.is_staff or
                self.request.user.pk == user_to_show.pk
        )
        return context


class UserProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileAvatarForm
    template_name = "myauth/user_profile_update.html"

    def test_func(self):
        user_pk = self.kwargs.get('pk')
        return self.request.user.is_staff or self.request.user.pk == user_pk

    def get_object(self, queryset=None):
        user_pk = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=user_pk)
        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={'created_by': self.request.user}
        )
        return profile

    def get_success_url(self):
        profile = self.get_object()
        return reverse("myauth:user-detail", kwargs={"pk": profile.user.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = self.get_object().user
        return context


class AboutMeView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ("avatar",)
    template_name = "myauth/about-me.html"
    success_url = reverse_lazy("myauth:about-me")

    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(
            user=self.request.user,
            defaults={'created_by': self.request.user}
        )
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)

        Profile.objects.create(user=self.object)

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password)

        login(request=self.request, user=user)

        return response


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/admin/')

        return render(request, 'myauth/login.html')

    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return redirect("/admin/")

    return render(request, "myauth/login.html", {"error": "Invalid login"})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect(reverse("myauth:login"))


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")


@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"cookie value: {value!r}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("session set!")


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"session value: {value!r}")


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})

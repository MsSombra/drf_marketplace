from app_account.forms import UserCreationForm
from app_account.models import Profile
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, UpdateView


class ProfileCreateView(View):
    def get(self, request: HttpRequest):
        pass

    def post(self, request: HttpRequest):
        pass


class UserLoginView(LoginView):
    template_name = "login.html"


class UserLogoutView(LogoutView):
    next_page = "/"


class ProfileDetailView(DetailView):
    # template_name
    model = Profile
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProfileUpdateView(UpdateView):
    # template_name
    model = Profile
    # fields
    context_object_name = "profile"

    def get_success_url(self):
        return reverse("app_account:profile_detail")

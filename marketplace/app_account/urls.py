from app_account.views import (ProfileCreateView, ProfileDetailView,
                               ProfileUpdateView, UserLoginView,
                               UserLogoutView)
from django.urls import path

app_name = "app_account"
urlpatterns = [
    path("sign_up/", ProfileCreateView.as_view(), name="registration"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("", ProfileDetailView.as_view(), name="profile_detail"),
    path("update/", ProfileUpdateView.as_view(), name="profile_update"),
]

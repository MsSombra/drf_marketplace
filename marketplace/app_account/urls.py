from app_account.views import (ProfileCreateView, UserLoginView,
                               UserLogoutView)
from django.urls import path

app_name = "app_account"
urlpatterns = [
    path("sign_up/", ProfileCreateView.as_view(), name="registration"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("", ..., name="profile_details_or_update"),
    path("password/", ..., name="profile_update_password"),
    path("avatar/", ..., name="profile_update_avatar"),
]

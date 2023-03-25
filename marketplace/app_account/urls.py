from app_account.views import (ProfileCreateView, ProfileDetailsView, PasswordUpdateView, AvatarUpdateView)
from django.urls import path

app_name = "app_account"
urlpatterns = [
    path("sign_up/", ProfileCreateView.as_view(), name="registration"),
    path("", ProfileDetailsView.as_view(), name="profile_details_or_update"),
    path("password/", PasswordUpdateView.as_view(), name="profile_update_password"),
    path("avatar/", AvatarUpdateView.as_view(), name="profile_update_avatar"),
]

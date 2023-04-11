from app_account.views import (AvatarUpdateView, PasswordUpdateView,
                               ProfileDetailsView)
from django.urls import path

app_name = "app_account"
urlpatterns = [
    path("", ProfileDetailsView.as_view(), name="profile_details_or_update"),
    path("password/", PasswordUpdateView.as_view(), name="profile_update_password"),
    path("avatar/", AvatarUpdateView.as_view(), name="profile_update_avatar"),
]

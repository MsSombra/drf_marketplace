from django.urls import path

from .views import AvatarUpdateView, PasswordUpdateView, ProfileDetailsView

app_name = "app_account"
urlpatterns = [
    path("", ProfileDetailsView.as_view(), name="profile_details_or_update"),
    path("password/", PasswordUpdateView.as_view(), name="profile_update_password"),
    path("avatar/", AvatarUpdateView.as_view(), name="profile_update_avatar"),
]

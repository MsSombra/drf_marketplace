
from django.urls import path

from app_settings.views import SettingsView

urlpatterns = [
    path("", SettingsView.as_view(), name="settings"),
]

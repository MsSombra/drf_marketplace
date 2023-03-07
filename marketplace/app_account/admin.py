from django.contrib import admin
from app_account.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = "pk", "user", "full_name"
    list_display_links = "pk", "user"

from django.contrib import admin

from app_account.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """ Представление профиля в админ панели """
    list_display = "pk", "user", "phone"
    list_display_links = list_display

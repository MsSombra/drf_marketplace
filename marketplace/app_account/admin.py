from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """ Представление профиля в админ панели """
    list_display = "pk", "user", "phone"
    list_display_links = list_display


# @admin.register(ProfileAvatar)
# class ProfileAvatarAdmin(admin.ModelAdmin):
#     list_display = "pk", "profile", "alt"
#     list_display_links = "pk", "profile"

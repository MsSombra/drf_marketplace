from app_account.models import Profile, ProfileAvatar
from django.contrib import admin


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = "pk", "user", "fullName"
    list_display_links = "pk", "user"


@admin.register(ProfileAvatar)
class ProfileAvatarAdmin(admin.ModelAdmin):
    list_display = "pk", "profile", "alt"
    list_display_links = "pk", "profile"

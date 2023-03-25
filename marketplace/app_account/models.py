from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile", verbose_name="пользователь")
    phone = PhoneNumberField(unique=True, null=False, blank=False, verbose_name="номер телефона")
    fullName = models.CharField(max_length=100, db_index=True, verbose_name="ФИО")

    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профили"


class ProfileAvatar(models.Model):
    image = models.ImageField(upload_to="profile_avatars/", blank=True, verbose_name="аватар")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="avatar", verbose_name="профиль")
    alt = models.CharField(max_length=20, verbose_name="описание")

    def __str__(self):
        return self.alt

    @property
    def src(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    class Meta:
        verbose_name = "аватар профиля"
        verbose_name_plural = "аватары профилей"

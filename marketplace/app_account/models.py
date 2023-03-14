from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile", verbose_name="пользователь")
    phone = PhoneNumberField(unique=True, null=False, blank=False, verbose_name="номер телефона")
    # avatar = models.ImageField(upload_to="profile_avatars/", blank=True, verbose_name="аватар")
    full_name = models.CharField(max_length=100, db_index=True, verbose_name="ФИО")

    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профили"

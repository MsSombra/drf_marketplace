from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    """ профиль пользователя (User) """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name="пользователь")
    phone = PhoneNumberField(unique=True, null=False, blank=True, verbose_name="номер телефона")
    avatar = models.ImageField(null=True, blank=True, upload_to="profile_avatars/", verbose_name="аватар")

    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профили"

    @property
    def fullName(self) -> str:
        """ Возвращает полное имя пользователя (имя и фамилия) """
        return " ".join([self.user.last_name, self.user.first_name])

    @fullName.setter
    def fullName(self, value: str):
        """ Устанавливает фамилию и имя пользователя """
        self.user.last_name, self.user.first_name, *_ = value.split()
        self.user.save()

    @property
    def email(self) -> str:
        """ Возвращает email пользователя """
        return self.user.email

    @email.setter
    def email(self, value: str):
        """ Устанавливает email пользователя """
        self.user.email = value
        self.user.save()

    def set_avatar(self, avatar):
        self.avatar = avatar
        self.save()

    def __str__(self):
        return f"Профиль пользователя {self.fullName}"

# class Profile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile", verbose_name="пользователь")
#     phone = PhoneNumberField(unique=True, null=False, blank=False, verbose_name="номер телефона")
#     fullName = models.CharField(max_length=100, db_index=True, verbose_name="ФИО")
#
#     class Meta:
#         verbose_name = "профиль"
#         verbose_name_plural = "профили"
#
#     def __str__(self):
#         return f"Профиль пользователя {self.fullName}"
#
#
# class ProfileAvatar(models.Model):
#     image = models.ImageField(upload_to="profile_avatars/", blank=True, verbose_name="аватар")
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="avatar", verbose_name="профиль")
#     alt = models.CharField(max_length=20, verbose_name="описание")
#
#     def __str__(self):
#         return self.alt
#
#     @property
#     def src(self):
#         if self.image and hasattr(self.image, 'url'):
#             return self.image.url
#
#     class Meta:
#         verbose_name = "аватар профиля"
#         verbose_name_plural = "аватары профилей"

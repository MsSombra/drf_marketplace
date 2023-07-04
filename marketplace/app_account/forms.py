from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import (PhoneNumberField,
                                          RegionalPhoneNumberWidget)


class ExtendedRegisterForm(UserCreationForm):
    """ Форма для создания нового профиля пользователя """
    phone = PhoneNumberField(required=False, widget=RegionalPhoneNumberWidget)

    class Meta(UserCreationForm):
        model = User
        fields = ("username", "first_name", "last_name", "email")

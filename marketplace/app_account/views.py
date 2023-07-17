from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app_account.models import Profile
from app_account.serializers import AvatarSerializer, ProfileSerializer


class ProfileDetailsView(RetrieveUpdateAPIView):
    """ Получение/обновление информации о профиле пользователя """
    serializer_class = ProfileSerializer

    def get_object(self) -> Profile:
        return Profile.objects.select_related("user").get(pk=self.request.user.profile.pk)


class PasswordUpdateView(APIView):
    """ Изменение пароля пользователя """
    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def put(self, request: Request) -> Response:
        """ Проверка правильности введенного текущего пароля и установка нового """
        obj: User = self.get_object()
        current_password = request.data.get("passwordCurrent")
        data = {"errors": "Введен некорректный текущий пароль"}

        if obj.check_password(current_password):
            obj.set_password(request.data.get("password"))
            obj.save()
            login(request, obj)
            del data["errors"]

        return Response(data)


class AvatarUpdateView(APIView):
    """ Установка/обновление аватара профиля """
    def get_object(self):
        return Profile.objects.get(pk=self.request.user.profile.pk)

    def post(self, request: Request, *args, **kwargs) -> Response:
        """ Установка/обновление аватара профиля """
        avatar: UploadedFile = request.FILES.get("avatar")
        obj: Profile = self.get_object()

        obj.set_avatar(avatar)
        profile_avatar = AvatarSerializer(obj)

        return Response(profile_avatar.data, status.HTTP_201_CREATED)

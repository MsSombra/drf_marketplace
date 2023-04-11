from app_account.models import Profile
from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from app_account.serializers import ProfileSerializer
from rest_framework.response import Response


class ProfileDetailsView(APIView):
    def get(self, request: HttpRequest):
        profile = Profile.objects.filter(user__id=self.request.user.id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request: HttpRequest):
        pass


class PasswordUpdateView(GenericAPIView):
    pass


class AvatarUpdateView(GenericAPIView):
    pass

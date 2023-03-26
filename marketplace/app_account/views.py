from django.http import HttpRequest
from django.urls import reverse
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin, UpdateModelMixin)

from app_account.models import Profile


class ProfileCreateView(CreateModelMixin, GenericAPIView):  # ListModelMixin
    def get(self, request: HttpRequest):
        pass

    def post(self, request: HttpRequest):
        pass


class ProfileDetailsView(UpdateModelMixin, RetrieveModelMixin, GenericAPIView):
    def get(self, request: HttpRequest):
        pass

    def post(self, request: HttpRequest):
        pass


class PasswordUpdateView(GenericAPIView):
    pass


class AvatarUpdateView(GenericAPIView):
    pass

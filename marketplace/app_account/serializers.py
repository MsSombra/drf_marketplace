from rest_framework import serializers
from app_account.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "id",  # "fullName", "phone", "avatar"
        # email?

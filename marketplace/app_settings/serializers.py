from rest_framework import serializers
from app_settings.models import SiteSettings


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = ["cost_express", "edge_for_free_delivery", "cost_usual_delivery"]

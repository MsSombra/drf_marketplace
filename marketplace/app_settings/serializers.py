from app_settings.models import SiteSettings
from rest_framework import serializers


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = ["cost_express_delivery", "edge_for_free_delivery", "cost_usual_delivery",
                  "popular_products_amount", "limited_products_amount", "banners_amount"]

from django.core.management import BaseCommand

from app_orders.models import DeliveryType
from app_settings.models import SiteSettings


class Command(BaseCommand):
    def handle(self, *args, **options):
        settings: SiteSettings = SiteSettings.load()

        DeliveryType.objects.get_or_create(type="regular", cost=settings.cost_usual_delivery)
        DeliveryType.objects.get_or_create(type="express", cost=settings.cost_express_delivery)

        self.stdout.write(self.style.SUCCESS("Delivery types created"))

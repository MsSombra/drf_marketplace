import sys

from app_settings.utils import SettingFileLoader
from django.apps import AppConfig

from marketplace import settings


class AppSettingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_settings'

    def ready(self):
        SiteSettings = self.get_model('SiteSettings')
        if ('makemigrations' not in sys.argv) and ('migrate' not in sys.argv):
            setting_conf = SettingFileLoader(settings.APP_SETTINGS_PATH)
            SiteSettings.objects.get_or_create(**setting_conf.config)

from django.db import models

from app_settings.singleton_model import SingletonModel


class SiteSettings(SingletonModel):
    cost_express = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена экспресс доставки")
    edge_for_free_delivery = models.DecimalField(max_digits=10, decimal_places=2,
                                                 verbose_name="Порог бесплатной доставки")
    cost_usual_delivery = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена обычной доставки")

    def __str__(self):
        return "конфигурация"

    class Meta:
        verbose_name = "конфигурация"
        verbose_name_plural = "конфигурация"

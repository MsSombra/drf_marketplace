from app_settings.singleton_model import SingletonModel
from django.db import models


class SiteSettings(SingletonModel):
    cost_express_delivery = models.DecimalField(max_digits=10, decimal_places=2,
                                                verbose_name="Цена экспресс доставки")
    edge_for_free_delivery = models.DecimalField(max_digits=10, decimal_places=2,
                                                 verbose_name="Порог бесплатной доставки")
    cost_usual_delivery = models.DecimalField(max_digits=10, decimal_places=2,
                                              verbose_name="Цена обычной доставки")
    popular_products_amount = models.PositiveSmallIntegerField(default=10,
                                                               verbose_name="количество популярных товаров для "
                                                                            "отображения на стартовой странице")
    limited_products_amount = models.PositiveSmallIntegerField(default=5,
                                                               verbose_name="количество товаров с ограниченным "
                                                                            "предложением для отображения на стартовой "
                                                                            "странице")
    banners_amount = models.PositiveSmallIntegerField(default=5,
                                                      verbose_name="количество баннеров"
                                                                   "для отображения на стартовой странице")

    def __str__(self):
        return "конфигурация"

    class Meta:
        verbose_name = "конфигурация"
        verbose_name_plural = "конфигурация"

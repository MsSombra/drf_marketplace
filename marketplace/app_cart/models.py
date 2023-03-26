from django.db import models

from app_account.models import Profile
from app_catalog.models import Product


class Basket(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='cart')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return f'Корзина {self.profile}'

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

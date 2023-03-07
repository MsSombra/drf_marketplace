from django.db import models
from app_catalog.models import Product


class Cart(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="сумма покупок")
    amount = models.PositiveIntegerField(verbose_name="количество")
    products = models.ManyToManyField(Product, related_name="cart", verbose_name="товары")
    free_delivery = models.BooleanField(default=False, verbose_name="бесплатная доставка")

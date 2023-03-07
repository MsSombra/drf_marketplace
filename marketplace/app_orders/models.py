from django.db import models
from app_catalog.models import Product
from app_account.models import Profile


class PaymentType(models.Model):
    title = models.CharField(max_length=40, verbose_name="название")

    class Meta:
        verbose_name = "тип оплаты"
        verbose_name_plural = "типы оплаты"

    def __str__(self):
        return self.title


class DeliveryType(models.Model):
    title = models.CharField(max_length=40, verbose_name="название")

    class Meta:
        verbose_name = "тип доставки"
        verbose_name_plural = "типы доставки"

    def __str__(self):
        return self.title


class OrderStatus(models.Model):
    title = models.CharField(max_length=40, verbose_name="название")

    class Meta:
        verbose_name = "статус заказа"
        verbose_name_plural = "статусы заказа"

    def __str__(self):
        return self.title


class Order(models.Model):
    products = models.ManyToManyField(Product, related_name="orders", verbose_name="товары")
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="orders", verbose_name="покупатель")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    payment_type = models.ForeignKey(PaymentType, related_name="orders", verbose_name="тип оплаты",
                                     on_delete=models.PROTECT)
    delivery_type = models.ForeignKey(DeliveryType, related_name="orders", verbose_name="тип доставки",
                                      on_delete=models.PROTECT)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="сумма заказа")
    status = models.ForeignKey(OrderStatus, related_name="orders", verbose_name="статус заказа",
                               on_delete=models.PROTECT)
    city = models.CharField(max_length=40, verbose_name="город")
    address = models.CharField(max_length=40, verbose_name="адрес")

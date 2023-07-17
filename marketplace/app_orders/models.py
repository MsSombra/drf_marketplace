from decimal import Decimal

from app_account.models import Profile
from app_catalog.models import Product
from app_payment.models import PaymentTypeChoices
from app_settings.models import SiteSettings
from django.db import models

from app_orders.choices import DeliveryChoices, StatusChoices


class OrderItem(models.Model):
    """ Модель товара в заказе """
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="product", verbose_name="заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items", verbose_name="товар")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='количество')

    class Meta:
        verbose_name = "товары"
        verbose_name_plural = "товары"

    @property
    def total_cost(self):
        return Decimal(self.price * self.quantity)

    def __str__(self):
        return f"Order {self.pk} - Product {self.product.name}"


class DeliveryType(models.Model):
    """ Модель типа доставки """
    type = models.CharField(choices=DeliveryChoices.choices,
                            max_length=10,
                            default=DeliveryChoices.regular,
                            verbose_name="тип")
    cost = models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Цена доставки")

    class Meta:
        verbose_name = "тип доставки"
        verbose_name_plural = "типы доставки"

    def save(self, *args, **kwargs) -> None:
        if self.type not in [d.type for d in DeliveryType.objects.all()]:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.type


class Order(models.Model):
    """ Модель заказа """
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="orders", verbose_name="покупатель")
    products = models.ManyToManyField(Product,
                                      through=OrderItem,
                                      through_fields=("order", "product"),
                                      verbose_name="товары")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    deliveryType = models.ForeignKey(DeliveryType,
                                     on_delete=models.PROTECT,
                                     related_name="orders",
                                     default=1,
                                     verbose_name="тип доставки")
    paymentType = models.CharField(choices=PaymentTypeChoices.choices,
                                   max_length=20,
                                   default=PaymentTypeChoices.own_online,
                                   verbose_name="тип оплаты")
    status = models.CharField(choices=StatusChoices.choices,
                              max_length=20,
                              default=StatusChoices.accepted,
                              verbose_name="статус платежа")
    city = models.CharField(max_length=40, default="", verbose_name="город")
    address = models.CharField(max_length=100, default="", verbose_name="адрес")

    class Meta:
        ordering = ('-createdAt',)
        verbose_name = "заказ"
        verbose_name_plural = "заказы"

    def product_price(self, product: Product):
        """ Возвращает цену товара"""
        item: OrderItem = OrderItem.objects.get(product=product, order=self)
        return item.price

    def product_count(self, product: Product):
        """ Возвращает количество товара """
        item: OrderItem = OrderItem.objects.get(product=product, order=self)
        return item.quantity

    def __str__(self):
        return f"Заказ #{self.pk} - {self.buyer.fullName}"

    def totalCost(self):
        """ Возвращает стоимость заказа (стоимость товаров, доставки) """
        items = OrderItem.objects.filter(order=self)
        items_cost = sum(i.total_cost for i in items)

        if not self.deliveryType:
            return items_cost

        if self.deliveryType.type == "regular":
            settings = SiteSettings.load()
            edge = settings.edge_for_free_delivery

            delivery = self.deliveryType.cost if items_cost < edge else 0
        else:
            delivery = self.deliveryType.cost

        return items_cost + delivery

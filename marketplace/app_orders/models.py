from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from app_account.models import Profile
from app_catalog.models import Product


class Order(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    fullName = models.CharField(max_length=100, db_index=True, verbose_name="ФИО")
    email = models.EmailField(max_length=50, blank=True, verbose_name="электронная почта")
    phone = PhoneNumberField(unique=True, null=False, blank=False, verbose_name="номер телефона")
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="orders", verbose_name="покупатель")
    deliveryType = models.CharField(max_length=30, verbose_name="тип доставки")
    paymentType = models.CharField(max_length=30, verbose_name="тип оплаты")
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена доставки', default=0)
    # totalCost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="сумма заказа")
    status = models.CharField(max_length=150, verbose_name='статус платежа', blank=True, null=True)
    city = models.CharField(max_length=40, verbose_name="город")
    address = models.CharField(max_length=40, verbose_name="адрес")
    card_number = models.PositiveIntegerField(validators=[MinValueValidator(10000000), MaxValueValidator(99999999)],
                                              verbose_name='Номер карты')
    payment_code = models.IntegerField(default=0, verbose_name='Код оплаты')
    # products = models.ManyToManyField(Product, related_name="orders", verbose_name="товары")

    class Meta:
        ordering = ('-createdAt',)
        verbose_name = "заказ"
        verbose_name_plural = "заказы"

    def __str__(self):
        return f"Заказ #{self.pk}"

    def totalCost(self):
        return sum(prod.get_cost() for prod in self.products.all()) + self.delivery_price


class ProductsInOrder(models.Model):
    order = models.ForeignKey(Order, related_name='products', on_delete=models.CASCADE, verbose_name='заказ')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name='товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='количество')

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = "товары"
        verbose_name_plural = "товары"

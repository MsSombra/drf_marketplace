from app_account.models import Profile
from app_catalog.models import Product
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class OrderStatus(models.Model):
    title = models.CharField(max_length=40, verbose_name="название")

    class Meta:
        verbose_name = "статус заказа"
        verbose_name_plural = "статусы заказа"

    def __str__(self):
        return self.title


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    full_name = models.CharField(max_length=100, db_index=True, verbose_name="ФИО")
    email = models.EmailField(max_length=50, blank=True, verbose_name="электронная почта")
    phone = PhoneNumberField(unique=True, null=False, blank=False, verbose_name="номер телефона")
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="orders", verbose_name="покупатель")
    deliveryType = models.CharField(max_length=30, verbose_name="тип доставки")
    paymentType = models.CharField(max_length=30, verbose_name="тип оплаты")
    totalCost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="сумма заказа")
    status = models.ForeignKey(OrderStatus, related_name="orders", verbose_name="статус заказа",
                               on_delete=models.PROTECT)
    city = models.CharField(max_length=40, verbose_name="город")
    address = models.CharField(max_length=40, verbose_name="адрес")
    products = models.ManyToManyField(Product, related_name="orders", verbose_name="товары")


class ProductsInOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="товар")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="заказ")
    amount = models.PositiveIntegerField(verbose_name="количество товара в заказе")

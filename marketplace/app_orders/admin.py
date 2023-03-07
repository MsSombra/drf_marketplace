from django.contrib import admin
from app_orders.models import OrderStatus, PaymentType, DeliveryType, Order


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = "pk", "title"
    list_display_links = "pk", "title"


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = "pk", "title"
    list_display_links = "pk", "title"


@admin.register(DeliveryType)
class DeliveryTypeAdmin(admin.ModelAdmin):
    list_display = "pk", "title"
    list_display_links = "pk", "title"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = "pk", "buyer", "created_at", "status"
    list_display_links = "pk", "buyer"

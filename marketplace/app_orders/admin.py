from django.contrib import admin

from app_orders.models import DeliveryType, Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = "pk", "buyer", "createdAt", "status"
    list_display_links = list_display


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = "pk", "product", "order"
    list_display_links = list_display


@admin.register(DeliveryType)
class DeliveryType(admin.ModelAdmin):
    list_display = "pk", "type", "cost"
    list_display_links = list_display

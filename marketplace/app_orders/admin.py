from app_orders.models import Order, OrderStatus
from django.contrib import admin


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = "pk", "title"
    list_display_links = "pk", "title"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = "pk", "buyer", "createdAt", "status"
    list_display_links = "pk", "buyer"

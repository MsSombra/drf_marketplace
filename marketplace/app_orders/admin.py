from app_orders.models import Order
from django.contrib import admin


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = "pk", "buyer", "createdAt", "status"
    list_display_links = "pk", "buyer"

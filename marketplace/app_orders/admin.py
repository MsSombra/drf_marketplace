from django.contrib import admin

from app_orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = "pk", "buyer", "createdAt", "status"
    list_display_links = "pk", "buyer"

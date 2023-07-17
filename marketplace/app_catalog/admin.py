from django.contrib import admin

from app_catalog.models import (Category, Product, ProductImage, Review, Sale,
                                Specification, Tag)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "pk", "title", "parent"
    list_display_links = list_display


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "value"
    list_display_links = list_display


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = "pk", "title", "category", "price", "available"
    list_display_links = list_display
    search_fields = ("title", "fullDescription")


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = "pk", "product"
    list_display_links = list_display


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = "pk", "author", "product"
    list_display_links = list_display


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = "pk", "product", "salePrice"
    list_display_links = list_display


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = "pk", "name"
    list_display_links = list_display

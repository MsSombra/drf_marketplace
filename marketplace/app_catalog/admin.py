from django.contrib import admin

from app_catalog.models import (Category, Product, ProductImage, Review,
                                Specification)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "pk", "name"
    list_display_links = "pk", "name"


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = "pk", "title", "description"
    list_display_links = "pk", "title"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "category", "price", "available"
    list_display_links = "pk", "name"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = "pk", "product"
    list_display_links = "pk", "product"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = "pk", "author", "product"
    list_display_links = "pk", "author"

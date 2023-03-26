from django.contrib import admin

from app_catalog.models import (Category, CategoryImage, Product, ProductImage,
                                Review, Sale, Specification, SubCategory,
                                SubCategoryImage, Tag)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "pk", "title"
    list_display_links = "pk", "title"


@admin.register(CategoryImage)
class CategoryImageAdmin(admin.ModelAdmin):
    list_display = "pk", "category", "alt"
    list_display_links = "pk", "category"


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = "pk", "title"
    list_display_links = "pk", "title"


@admin.register(SubCategoryImage)
class SubCategoryImageAdmin(admin.ModelAdmin):
    list_display = "pk", "subcategory", "alt"
    list_display_links = "pk", "subcategory"


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "value"
    list_display_links = "pk", "name"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = "pk", "title", "category", "price", "available"
    list_display_links = "pk", "title"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = "pk", "product"
    list_display_links = "pk", "product"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = "pk", "author", "product"
    list_display_links = "pk", "author"


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = "pk", "product", "salePrice"
    list_display_links = "pk", "product"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = "pk", "name"
    list_display_links = "pk", "name"

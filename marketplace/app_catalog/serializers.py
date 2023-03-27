from rest_framework import serializers

from app_catalog.models import (
    Tag, Category, CategoryImage,
    SubCategory, SubCategoryImage,
    )


class SubCategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategoryImage
        fields = ["alt", "src"]


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "title", "image", "href"]
        depth = 2


class CategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryImage
        fields = ["alt", "src"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "image", "href", "subcategories"]
        depth = 1


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]

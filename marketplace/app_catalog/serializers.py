from rest_framework import serializers

from app_catalog.models import (
    Tag, Category, CategoryImage,
    )


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class FilterCategoryListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class CategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryImage
        fields = ["alt", "src"]


class CategorySerializer(serializers.ModelSerializer):
    subcategories = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterCategoryListSerializer
        model = Category
        fields = ["id", "title", "image", "href", "subcategories"]
        depth = 1


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]

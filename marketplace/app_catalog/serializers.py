from rest_framework import serializers
from time import strftime

from app_catalog.models import (
    Tag, Category, CategoryImage,
    Product,
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
        fields = "__all__"


class RelatedFieldAlternative(serializers.PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        self.serializer = kwargs.pop('serializer', None)
        if self.serializer is not None and not issubclass(self.serializer, serializers.Serializer):
            raise TypeError('"serializer" is not a valid serializer class')

        super().__init__(**kwargs)

    def use_pk_only_optimization(self):
        return False if self.serializer else True

    def to_representation(self, instance):
        if self.serializer:
            return self.serializer(instance, context=self.context).data
        return super().to_representation(instance)


class CategorySerializer(serializers.ModelSerializer):
    subcategories = RecursiveSerializer(many=True)
    image = RelatedFieldAlternative(queryset=CategoryImage.objects.all(), serializer=CategoryImageSerializer)

    class Meta:
        model = Category
        list_serializer_class = FilterCategoryListSerializer
        fields = ["id", "title", "image", "href", "subcategories"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="id", read_only=True)
    price = serializers.IntegerField()
    date = serializers.SerializerMethodField(method_name="get_date_format")
    images = serializers.SlugRelatedField(slug_field="image", read_only=True, many=True)
    tags = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)

    class Meta:
        model = Product
        fields = ["id", "category", "price", "count", "date", "title", "description", "fullDescription", "href",
                  "freeDelivery", "images", "tags", "specifications", "reviews", "rating", "available",
                  "hot_offer", "limited_edition"]
        depth = 1

    def get_date_format(self, obj):
        fmt = "The %b %d %Y %I:%M:%S %Z%z"
        return obj.date.strftime(fmt)

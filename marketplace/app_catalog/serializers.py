import datetime

from rest_framework import serializers

from app_catalog.models import Category, Product, Review, Sale, Tag


class RecursiveSerializer(serializers.Serializer):
    """ Сериализатор для отображения подкатегорий """
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class FilterCategoryListSerializer(serializers.ListSerializer):
    """ Сериализатор для фильтрации категорий, являющихся родительскими """
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        list_serializer_class = FilterCategoryListSerializer
        fields = ("id", "title", "image", "href", "subcategories")

    subcategories = RecursiveSerializer(many=True)


class TagSerializer(serializers.ModelSerializer):
    """ Сериализатор тэгов товара """
    class Meta:
        model = Tag
        fields = ("id", "name")


class ReviewSerializer(serializers.ModelSerializer):
    """ Сериализатор отзыва на товар """
    class Meta:
        model = Review
        exclude = ("id", "product")
        optional_fields = ("product_id", )

    product_id = serializers.IntegerField(source="product.id")
    date = serializers.SerializerMethodField("get_date_formatted")

    @classmethod
    def get_date_formatted(cls, obj: Review) -> str:
        return datetime.datetime.strftime(obj.date, "%H:%M %Y-%m-%d")

    def create(self, validated_data):
        product_id = validated_data.pop("product")["id"]
        return Review.objects.create(product_id=product_id, **validated_data)


class ProductSerializer(serializers.ModelSerializer):
    """ Сериализатор товара (полный вариант) """
    class Meta:
        model = Product
        fields = ("id", "category", "price", "count", "date", "title", "description", "fullDescription", "href",
                  "freeDelivery", "images", "tags", "specifications", "reviews", "rating")
        depth = 1

    category = serializers.SlugRelatedField(slug_field="id", read_only=True)
    tags = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    rating = serializers.FloatField()
    price = serializers.IntegerField()
    reviews = ReviewSerializer(many=True)
    date = serializers.SerializerMethodField(method_name="get_date_format")
    images = serializers.SerializerMethodField('get_images')

    @classmethod
    def get_date_format(cls, obj: Product) -> str:
        fmt = "The %b %d %Y %I:%M:%S %Z%z"
        return obj.date.strftime(fmt)

    @classmethod
    def get_images(cls, obj: Product):
        return [i.image.url for i in obj.images.all()]


class ProductShortSerializer(ProductSerializer):
    """ Укороченная версия сериализатора товара """
    class Meta(ProductSerializer.Meta):
        optional_fields = ('tags',)

    reviews = serializers.SerializerMethodField("get_reviews_amount")

    @classmethod
    def get_reviews_amount(cls, obj: Product) -> int:
        return obj.reviews.count()


class SaleSerializer(serializers.ModelSerializer):
    """ Сериализатор скидок на товары """
    class Meta:
        model = Sale
        fields = ("id", "price", "salePrice", "dateFrom", "dateTo", "title", "href", "images")

    id = serializers.IntegerField(source="product.id")
    price = serializers.DecimalField(source="product.price", decimal_places=2, max_digits=10)
    title = serializers.CharField(source="product.title")
    href = serializers.CharField(source="product.href")
    images = serializers.SerializerMethodField("get_images")

    @classmethod
    def get_images(cls, obj: Sale):
        return [i.image.url for i in obj.product.images.all()]

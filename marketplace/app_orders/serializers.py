from rest_framework import serializers

from app_orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """ Сериализатор заказа """
    class Meta:
        model = Order
        fields = (
            "orderId",
            "createdAt",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "products"
        )
        depth = 1

    orderId = serializers.SerializerMethodField("get_order_id")
    createdAt = serializers.SerializerMethodField(method_name="get_date_format")

    fullName = serializers.CharField(source="buyer.fullName")
    phone = serializers.CharField(source="buyer.phone")
    email = serializers.EmailField(source="buyer.email")

    deliveryType = serializers.CharField(source="deliveryType.type")
    products = serializers.SerializerMethodField("get_products")

    @classmethod
    def get_order_id(cls, obj: Order):
        return obj.pk

    @classmethod
    def get_date_format(cls, obj: Order) -> str:
        fmt = "%Y-%m-%d %H:%M"
        return obj.createdAt.strftime(fmt)

    @classmethod
    def get_products(cls, obj: Order) -> list[dict]:
        return [
            {
                "id": p.pk,
                "category": p.category.pk,
                "price": obj.product_price(p),
                "count": obj.product_count(p),
                "date": p.date,
                "title": p.title,
                "description": p.description,
                "href": p.href,
                "freeDelivery": p.freeDelivery,
                "images": [i.image.url for i in p.images.all()],
                "tags": [i.name for i in p.tags.all()],
                "reviews": p.reviews.count(),
                "rating": p.rating
            }
            for p in obj.products.all()
        ]

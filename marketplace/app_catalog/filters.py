import django_filters as filters

from app_catalog.models import Product


class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = ["available"]

    sort = filters.OrderingFilter(
        fields=(
            ("price", "price"),
            ("date", "date"),
            ("_reviews", "reviews"),
            ("_order_items", 'rating')
        )
    )

    minPrice = filters.NumberFilter(field_name="price", lookup_expr="gte")
    maxPrice = filters.NumberFilter(field_name="price", lookup_expr="lte")
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    available = filters.BooleanFilter(
        field_name="count", method="check_available"
    )
    freeDelivery = filters.BooleanFilter(
        field_name="freeDelivery", method="check_delivery"
    )

    @classmethod
    def check_available(cls, queryset, name, value):
        lookup = "__".join([name, "gt"])
        return queryset.filter(**{lookup: 0})

    @classmethod
    def check_delivery(cls, queryset, name, value):
        if value == "true":
            return queryset.filter(freeDelivery=True)
        return queryset

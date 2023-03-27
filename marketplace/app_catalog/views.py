from django.http import HttpRequest
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin)

from app_catalog.models import Tag, Category
from app_catalog.serializers import TagSerializer, CategorySerializer


class CategoryListView(ListModelMixin, GenericAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related("subcategories").all()

    def get(self, request: HttpRequest):
        return self.list(request)


class ProductListView(ListModelMixin, GenericAPIView):
    pass


class CategoryProductListView(ListModelMixin, GenericAPIView):
    pass


class ProductPopularView(ListModelMixin, GenericAPIView):
    pass


class ProductLimitedView(ListModelMixin, GenericAPIView):
    pass


class ProductSalesView(ListModelMixin, GenericAPIView):
    pass


class ProductBannersView(ListModelMixin, GenericAPIView):
    pass


class TagListView(ListModelMixin, GenericAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    def get(self, request: HttpRequest):
        return self.list(request)


class ProductDetailView(RetrieveModelMixin, GenericAPIView):
    pass


class ReviewCreateView(CreateModelMixin, GenericAPIView):
    pass

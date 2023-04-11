from app_catalog.models import Category, Product, Tag
from app_catalog.serializers import (CategorySerializer, ProductSerializer,
                                     TagSerializer)
from django.http import HttpRequest
from rest_framework import pagination
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            "currentPage": self.page.number,
            "lastPage": self.page.paginator.num_pages,
            "count": self.page.paginator.count,
            "items": data
        })


class CategoryListView(ListModelMixin, GenericAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related("subcategories").all()
    pagination_class = None

    def get(self, request: HttpRequest):
        return self.list(request)


class ProductListView(ListModelMixin, GenericAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = CustomPagination

    def get(self, request: HttpRequest):
        return self.list(request)


class CategoryProductListView(ListModelMixin, GenericAPIView):
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def get(self, request: HttpRequest, pk):
        return self.list(request)

    def get_queryset(self):
        pk = self.request.META['PATH_INFO'][13]
        qs = Product.objects.filter(category__id=pk).all()
        return qs


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
    pagination_class = None

    def get(self, request: HttpRequest):
        return self.list(request)


class ProductDetailView(RetrieveModelMixin, GenericAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = None

    def get(self, request: HttpRequest, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ReviewCreateView(CreateModelMixin, GenericAPIView):
    pass

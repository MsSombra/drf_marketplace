from django.http import HttpRequest
from rest_framework import pagination
from rest_framework.generics import (CreateAPIView, ListAPIView, RetrieveAPIView)
from rest_framework.response import Response

from app_catalog.models import Category, Product, Review, Sale, Tag
from app_catalog.serializers import (CategorySerializer, ProductSerializer,
                                     ProductShortSerializer, ReviewSerializer,
                                     SaleSerializer, TagSerializer)


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            "currentPage": self.page.number,
            "lastPage": self.page.paginator.num_pages,
            "count": self.page.paginator.count,
            "items": data
        })


class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related("subcategories").all()
    pagination_class = None


class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = CustomPagination


# class CategoryProductListView(ListModelMixin, GenericAPIView):
#     serializer_class = ProductSerializer
#     pagination_class = CustomPagination
#
#     def get(self, request: HttpRequest, pk):
#         return self.list(request)
#
#     def get_queryset(self):
#         pk = self.request.META['PATH_INFO'][13]
#         qs = Product.objects.filter(category__id=pk).all()
#         return qs


class ProductPopularView(ListAPIView):
    pass


class ProductLimitedView(ListAPIView):
    pass


class ProductSalesView(ListAPIView):
    pass


class ProductBannersView(ListAPIView):
    pass


class TagListView(ListAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.prefetch_related(
            "reviews", "tags", "category", "images", "specifications"
        ).all()
    pagination_class = None

    def get(self, request: HttpRequest, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ReviewCreateView(CreateAPIView):
    pass

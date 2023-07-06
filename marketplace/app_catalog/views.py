import re

from django.db.models import Avg, Sum, Count
from django.http import HttpRequest
from rest_framework import pagination, status
from rest_framework.generics import (CreateAPIView, ListAPIView, RetrieveAPIView)
from rest_framework.response import Response

from app_catalog.filters import ProductFilter
from app_catalog.models import Category, Product, Review, Sale, Tag
from app_catalog.serializers import (CategorySerializer, ProductSerializer,
                                     ProductShortSerializer, ReviewSerializer,
                                     SaleSerializer, TagSerializer)
from app_settings.models import SiteSettings


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            "currentPage": self.page.number,
            "lastPage": self.page.paginator.num_pages,
            "count": self.page.paginator.count,
            "items": data
        })


class CategoryListView(ListAPIView):
    """ Возвращает информацию о категориях """
    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related("subcategories").all()
    pagination_class = None


class ProductListView(ListAPIView):
    """ Возвращает список всех товаров. Позволяет применить к ним фильтры (кроме выбора категории) """
    pagination_class = CustomPagination
    serializer_class = ProductShortSerializer

    def get_queryset(self):
        qs = (
            Product.objects
            .annotate(_rating=Avg("reviews__rate"))
            .annotate(_order_items=Sum("order_items__quantity"))
            .annotate(_reviews=Count("reviews"))
        ).order_by("price")

        if tags := self.request.query_params.getlist("tags[]"):
            qs = qs.filter(tags__id__in=tags)

        qs = ProductFilter(data=self.request.query_params, queryset=qs)

        return qs.qs


class CategoryProductListView(ListAPIView):
    """ Возвращает товары выбранной категории  (по ее id) """
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        pattern = r"\/[\d]*\/"
        url = self.request.META['PATH_INFO']
        pk = re.findall(pattern, url)[1][1:-1]
        qs = Product.objects.filter(category__id=pk).all()
        return qs


class ProductPopularView(ListAPIView):
    """ Возвращает товары с самым высоким рейтингом. Количество к выводу задается в настройках """
    serializer_class = ProductShortSerializer
    pagination_class = None

    def get_queryset(self):
        qs = Product.objects.all()
        settings = SiteSettings.load()
        index = settings.popular_products_amount

        return qs.alias(rating=Avg("reviews__rate")).order_by("-rating")[:index]


class ProductLimitedView(ListAPIView):
    """ Возвращает товары, отмеченные как ограниченный тираж. Количество к выводу задается в настройках """
    serializer_class = ProductShortSerializer
    pagination_class = None

    def get_queryset(self):
        qs = Product.objects.all()
        settings = SiteSettings.load()
        index = settings.limited_products_amount

        return qs.filter(limited_edition=True)[:index]


class ProductSalesView(ListAPIView):
    """ Возвращает информацию о скидках на товары """
    queryset = Sale.objects.select_related("product")
    serializer_class = SaleSerializer
    pagination_class = None


class ProductBannersView(ListAPIView):
    """ Возвращает товары для /banners. Количество к выводу задается в настройках """
    serializer_class = ProductShortSerializer
    pagination_class = None

    def get_queryset(self):
        qs = Product.objects.all()
        settings = SiteSettings.load()
        index = settings.banners_amount

        return qs[:index]


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
    serializer_class = ReviewSerializer
    pagination_class = None

    def get_queryset(self):
        pattern = r"\/[\d]*\/"
        url = self.request.META['PATH_INFO']
        pk = re.findall(pattern, url)[0][1:-1]
        return Review.objects.select_related("product").filter(product_id=pk)

    def create(self, request, *args, **kwargs):
        pattern = r"\/[\d]*\/"
        url = self.request.META['PATH_INFO']
        pk = re.findall(pattern, url)[0][1:-1]

        request.data._mutable = True
        request.data.update({"product_id": pk})
        request.data._mutable = False

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        all_reviews = self.get_serializer(data=self.get_queryset(), many=True)
        all_reviews.is_valid()

        return Response(all_reviews.data, status=status.HTTP_201_CREATED)

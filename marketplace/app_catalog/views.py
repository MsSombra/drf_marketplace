from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin


class CategoryListView(ListModelMixin, GenericAPIView):
    pass


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
    pass


class ProductDetailView(RetrieveModelMixin, GenericAPIView):
    pass


class ReviewCreateView(CreateModelMixin, GenericAPIView):
    pass

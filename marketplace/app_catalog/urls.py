from django.urls import path

from app_catalog.views import (CategoryListView, # CategoryProductListView,
                               ProductBannersView, ProductDetailView,
                               ProductLimitedView, ProductListView,
                               ProductPopularView, ProductSalesView,
                               ReviewCreateView, TagListView)

app_name = "app_catalog"
urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("catalog/", ProductListView.as_view(), name="product_list"),
    # path("catalog/<int:pk>/", CategoryProductListView.as_view(), name="product_list_by_category"),
    path("products/popular/", ProductPopularView.as_view(), name="product_popular"),
    path("products/limited/", ProductLimitedView.as_view(), name="product_limited"),
    path("sales/", ProductSalesView.as_view(), name="product_sales"),
    path("banners/", ProductBannersView.as_view(), name="product_banners"),
    path("tags/", TagListView.as_view(), name="tag_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/<int:pk>/review/", ReviewCreateView.as_view(), name="review_create"),
]

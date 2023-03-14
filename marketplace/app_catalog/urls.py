from django.urls import path

app_name = "app_catalog"
urlpatterns = [
    path("categories/", ..., name="category_list"),
    path("catalog/", ..., name="product_list"),
    path("catalog/<int:pk>/", ..., name="product_list_by_category"),
    path("products/popular/", ..., name="product_popular"),
    path("products/limited/", ..., name="product_limited"),
    path("sales/", ..., name="product_sales"),
    path("banners/", ..., name="product_banners"),
    path("tags/", ..., name="tag_list"),
    path("product/<int:pk>/", ..., name="product_list"),
    path("product/<int:pk>/review/", ..., name="review_create"),
]

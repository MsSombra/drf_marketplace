from django.urls import path

app_name = "app_orders"
urlpatterns = [
    path("", ..., name="order_list"),
    path("<int:pk>/", ..., name="order_detail"),
    path("active/", ..., name="order_active"),
]

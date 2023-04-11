from app_orders.views import (OrderActiveListView, OrderDetailView,
                              OrderListView)
from django.urls import path

app_name = "app_orders"
urlpatterns = [
    path("", OrderListView.as_view(), name="order_list"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("active/", OrderActiveListView.as_view(), name="order_active"),
]

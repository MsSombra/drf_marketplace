from app_cart.views import CartView
from django.urls import path

app_name = "app_cart"
urlpatterns = [
    path("", CartView.as_view(), name="cart"),
]

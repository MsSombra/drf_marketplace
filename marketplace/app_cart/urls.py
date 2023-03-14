from app_cart.views import cart_add, cart_detail, cart_remove
from django.urls import path

app_name = "app_cart"
urlpatterns = [
    path("", ..., name="cart"),
]

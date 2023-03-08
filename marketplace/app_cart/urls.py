from app_cart.views import cart_add, cart_detail, cart_remove
from django.urls import path

app_name = "app_cart"
urlpatterns = [
    path("", cart_detail, name="cart"),
    path("add/", cart_add, name="add_to_cart"),
    path("remove/", cart_remove, name="remove_from_cart"),
]

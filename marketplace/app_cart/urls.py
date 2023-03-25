from django.urls import path
from app_cart.views import CartView

app_name = "app_cart"
urlpatterns = [
    path("", CartView.as_view(), name="cart"),
]

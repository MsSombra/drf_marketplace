from app_payment.views import PaymentView
from django.urls import path

app_name = "app_payment"
urlpatterns = [
    path("", PaymentView.as_view(), name="payment"),
]

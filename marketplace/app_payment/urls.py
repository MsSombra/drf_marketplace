from django.urls import path

from app_payment.views import PaymentView

app_name = "app_payment"
urlpatterns = [
    path("", PaymentView.as_view(), name="payment"),
]

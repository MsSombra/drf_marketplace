from rest_framework.views import APIView
from django.db.transaction import atomic
from rest_framework.request import Request
from rest_framework.response import Response
from app_orders.models import Order, OrderItem
from app_payment.services import is_payment_valid, check_amount, reduce_product_quantity
from rest_framework import status


class PaymentView(APIView):
    """ Проверяет возможность оплаты, наличие достаточного количества товаров """
    @atomic
    def post(self, request: Request, *args, **kwargs) -> Response:
        data = self.request.data

        # getting orders of request user which status is `awaiting payment`
        order_to_pay = (
            Order.objects
            .prefetch_related("product")
            .filter(buyer=self.request.user.profile, status="awaiting payment")
        )

        card_number = data.get("number")
        if not is_payment_valid(card_number):
            return Response(
                {"detail": "card number %s is not valid" % card_number},
                status=status.HTTP_400_BAD_REQUEST
            )

        items = (
            OrderItem.objects
            .prefetch_related("product")
            .filter(order__in=order_to_pay)
        )

        check = check_amount(items)
        if check == []:
            # if all products have enough amount reduce it with quantity in OrderItem
            reduce_product_quantity(items)
            order_to_pay.update(status="paid")
            self.request.cart.clear()

            return Response(status=status.HTTP_200_OK)

        return Response({"detail": check})

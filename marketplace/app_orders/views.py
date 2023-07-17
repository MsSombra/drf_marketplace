from app_catalog.models import Product
from django.contrib import messages
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404, redirect
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app_orders.models import DeliveryType, Order, OrderItem
from app_orders.serializers import OrderSerializer


class OrderListView(ListCreateAPIView):
    """ Создание нового заказа, получение информации о заказах текущего пользователя """
    serializer_class = OrderSerializer
    pagination_class = None

    def get_queryset(self) -> QuerySet[Order]:
        return Order.objects.filter(buyer=self.request.user.profile).order_by("-createdAt")

    def post(self, request: Request, *args, **kwargs) -> Response:
        if not request.user.is_authenticated:
            messages.error(request, "Необходимо авторизоваться")
            return redirect(request.META.get('HTTP_REFERER'))

        data = self.request.data

        new_data = {
            d["id"]: {
                "count": d["count"],
                "price": d["price"]
            }
            for d in data
        }
        products = Product.objects.filter(id__in=new_data.keys())

        order, created = Order.objects.get_or_create(
            buyer=self.request.user.profile, status="accepted"
        )

        if created:
            self.request.cart.clear()
            for p in products:
                p_id = p.id
                OrderItem.objects.create(
                    order=order,
                    product=p,
                    quantity=new_data[p_id]["count"],
                    price=new_data[p_id]["price"]
                )
        serializer = self.get_serializer()
        return Response(serializer.data)


class OrderDetailView(RetrieveModelMixin, GenericAPIView):
    """ Изменение/подтверждение заказа """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = None

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.retrieve(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs) -> Response:
        data = self.request.data
        buyer = self.request.user.profile

        order = Order.objects.get(
            buyer=buyer, status="accepted"
        )

        order.status = "awaiting payment"
        order.address = data.get("address", "")
        order.city = data.get("city", "")
        delivery_type = data.get("deliveryType", "regular")
        dt = DeliveryType.objects.get(type=delivery_type)
        order.deliveryType = dt
        order.paymentType = data.get("paymentType", "own online")
        order.save()
        messages.success(request, "Заказ успешно создан")
        return Response(status=status.HTTP_201_CREATED)


class OrderActiveListView(APIView):
    """ Возвращает заказы текущего пользователя в статусе accepted """
    serializer_class = OrderSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_204_NO_CONTENT)

        buyer = self.request.user.profile
        active_order = get_object_or_404(Order, buyer=buyer, status='accepted')
        serializer = self.serializer_class(active_order)
        return Response(serializer.data)

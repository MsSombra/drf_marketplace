from app_catalog.models import Product
from app_catalog.serializers import ProductShortSerializer
from django.db.models import QuerySet
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from app_cart.cart import Cart


class CartView(GenericAPIView):
    """ Для работы с товарами в корзине (добавление/изменение/удаление) """
    serializer_class = ProductShortSerializer
    pagination_class = None

    def get_cart(self) -> Cart:
        """ Получение информации о корзине из request """
        return self.request.cart

    def get_queryset(self) -> QuerySet[Product]:
        """ Получение информации по товарам, добавленным в корзину """
        cart = self.get_cart()
        return Product.objects.filter(id__in=cart.products.keys())

    def get_response(self) -> Response:
        """ Обработка данных для response """
        cart = self.get_cart()
        serializer = self.get_serializer(cart, many=True)
        return Response(serializer.data)

    def get(self, request: Request, *args, **kwargs) -> Response:
        """ Возвращает данные о корзине """
        return self.get_response()

    def get_product_info(self) -> tuple[Product, str]:
        """ Получение экземпляра класса Product и количества для действия в корзине """
        data = self.request.data
        qp = self.request.query_params

        product_id: str = data.get("id") or qp.get("id")
        amount: str = data.get("count") or qp.get("count")

        product = Product.objects.get(pk=product_id)
        return product, amount

    def post(self, *args, **kwargs) -> Response:
        """ Добавление товара в корзину """
        cart = self.get_cart()
        cart.add(*self.get_product_info())

        return self.get_response()

    def delete(self, *args, **kwargs) -> Response:
        """ Удаление товара из корзины """
        cart = self.get_cart()
        cart.reduce(*self.get_product_info())

        return self.get_response()

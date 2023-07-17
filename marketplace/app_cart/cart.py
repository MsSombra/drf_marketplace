import json
from decimal import Decimal

from app_catalog.models import Product
from django.conf import settings


class Cart:
    def __init__(self, session) -> None:
        """ Создание корзины """
        self.session = session
        products = self.session.get(settings.CART_SESSION_ID)
        if not products:
            products = self.session[settings.CART_SESSION_ID] = {}
        self.products = products

    def __iter__(self) -> Product:
        product_ids = self.products.keys()
        qs = Product.objects.filter(id__in=product_ids).values()

        cart = self.products

        for product in qs:
            product_id = str(product["id"])
            product["count"] = cart.get(product_id)["count"]
            product["price"] = cart.get(product_id)["price"]
            yield Product(**product)

    def __repr__(self):
        return json.dumps(self.products)

    def add(self, product, quantity: str = "1") -> None:
        """ Добавление товара в корзину или изменение его количества """
        product_id = str(product.pk)
        if product_id not in self.products.keys():
            self.products[product_id] = {
                "count": quantity,
                "price": str(product.price)
            }
        else:
            self.products[product_id]["count"] += int(quantity)

        self.save()

    def reduce(self, product, quantity: str) -> None:
        """ Уменьшить количество товара или убрать его из корзины """
        product_id = str(product.id)

        if product_id not in self.products.keys():
            return

        if quantity is None or self.products[product_id]["count"] <= 1:
            self.remove(product)
        else:
            self.products[product_id]["count"] -= int(quantity)

        self.save()

    def save(self) -> None:
        """ Отмечает сессию измененной для сохранения """
        self.session.modified = True

    def remove(self, product) -> None:
        """ Удалить товар из корзины """
        product_id = str(product.id)
        if product_id in self.products:
            del self.products[product_id]
            self.save()

    def clear(self) -> None:
        """ Удаляет корзину из сессии """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_cost(self):
        """ Возвращает стоимость всех товаров в корзине """
        return sum(
            Decimal(item["price"] * item["count"])
            for item in self.products.values()
        )

    def all(self):
        return [product for product in self.products.values()]

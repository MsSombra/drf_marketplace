from decimal import Decimal

from app_cart.models import Basket
from app_catalog.models import Product
from django.conf import settings
from django.db.models import F, Sum
from django.http import HttpRequest


class Cart(object):
    def __init__(self, request: HttpRequest):
        self.use_db = False
        self.cart = None
        self.user = request.user
        self.session = request.session
        self.qs = None

        cart = self.session.get(settings.CART_SESSION_ID)

        if self.user.is_authenticated:
            self.use_db = True
            if cart:
                self.save_in_db(cart, request.user)
                self.clear(True)
            self.qs = Basket.objects.filter(profile=self.user.profile)
            cart = self.get_cart_from_db(self.qs)
        else:
            if not cart:
                cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def get_cart_from_db(self, qs):
        cart = {}
        for elem in qs:
            cart[str(elem.product.id)] = {"product": elem.product, "quantity": elem.quantity, "price": elem.price}
        return cart

    def save_in_db(self, cart, user):
        for key, val in cart.items():
            if Basket.objects.filter(profile=user.profile, product=key).exists():
                good = Basket.objects.select_for_update().get(profile=user.profile, product=key)
                good.quantity += cart[key]["quantity"]
                good.price = cart[key]["price"]
                good.save()
            else:
                product = Product.objects.get(id=key)
                Basket.objects.create(
                    profile=user.profile,
                    product=product,
                    quantity=val["quantity"],
                    price=val["price"],
                )

    def add(self, product, quantity=1, update_quantity=False):
        if self.use_db:
            if self.qs.filter(product=product).exists():
                cart = self.qs.select_for_update().get(product=product)
            else:
                cart = Basket(
                    profile=self.user.profile,
                    product=product,
                    quantity=0,
                    price=product.price,
                )
            if update_quantity:
                cart.quantity = quantity
            else:
                cart.quantity += quantity
            cart.save()

        else:
            product_id = str(product.id)
            if product_id not in self.cart:
                self.cart[product_id] = {"quantity": 0, "price": str(product.price)}
            if update_quantity:
                self.cart[product_id]["quantity"] = quantity
            else:
                self.cart[product_id]["quantity"] += quantity
            self.save()

    def save(self):
        if not self.use_db:
            self.session[settings.CART_SESSION_ID] = self.cart
            self.session.modified = True

    def remove(self, product):
        if self.use_db:
            if self.qs.filter(product=product).exists():
                self.qs.filter(product=product).delete()
        else:
            product_id = str(product.id)
            if product_id in self.cart:
                del self.cart[product_id]
                self.save()

    def __iter__(self):
        if self.use_db:
            for elem in self.cart.values():
                elem["total_price"] = elem["price"] * elem["quantity"]
                yield elem
        else:
            product_ids = self.cart.keys()
            products = Product.objects.filter(id__in=product_ids)

            for product in products:
                self.cart[str(product.id)]["product"] = product

            for elem in self.cart.values():
                elem["price"] = Decimal(elem["price"])
                elem["total_price"] = elem["price"] * elem["quantity"]
                yield elem

    def __len__(self):
        return sum(elem["quantity"] for elem in self.cart.values())

    def get_total_price(self):
        if self.use_db:
            total = self.qs.only("quantity", "price").aggregate(total=Sum(F("quantity") * F("price")))["total"]
            if not total:
                total = 0
            return total
        else:
            return sum(Decimal(elem["price"]) * elem["quantity"] for elem in self.cart.values())

    def clear(self, only_session=False):
        if only_session:
            del self.session[settings.CART_SESSION_ID]
            self.session.modified = True
        else:
            if self.qs:
                self.qs.delete()

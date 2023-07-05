from django.http import HttpRequest, HttpResponse

from app_cart.cart import Cart


class SetCartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        request.cart = Cart(request.session)
        response = self.get_response(request)
        return response

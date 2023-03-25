from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin


class CartView(CreateModelMixin, GenericAPIView):
    def get(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass

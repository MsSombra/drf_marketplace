from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin


class OrderListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    pass


class OrderDetailView(RetrieveModelMixin, GenericAPIView):
    pass


class OrderActiveListView(RetrieveModelMixin, GenericAPIView):
    pass

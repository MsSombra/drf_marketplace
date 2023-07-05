from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.views import APIView


class OrderListView(ListCreateAPIView):
    pass


class OrderDetailView(RetrieveModelMixin, GenericAPIView):
    pass


class OrderActiveListView(APIView):
    pass

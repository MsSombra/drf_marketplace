from django.shortcuts import render
from django.views.decorators.http import require_POST


@require_POST
def cart_add(request, product_id, count):
    pass


def cart_remove(request, product_id, count):
    pass


def cart_detail(request):
    pass

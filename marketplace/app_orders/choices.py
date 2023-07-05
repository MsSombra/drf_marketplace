from django.db import models


class DeliveryChoices(models.TextChoices):
    regular = "regular"
    express = "express"


class StatusChoices(models.TextChoices):
    accepted = "accepted"
    awaiting_payment = "awaiting payment"
    paid = "paid"
    delivered = "delivered"

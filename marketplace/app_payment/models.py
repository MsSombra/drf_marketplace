from django.db import models


class PaymentTypeChoices(models.TextChoices):
    own_online = "own online"
    someone_online = "someone online"

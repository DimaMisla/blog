from django.db import models

from accounts.models import CustomUser


class Weather(models.Model):
    city = models.CharField(max_length=50)
    user = models.ManyToManyField(CustomUser,
                                  related_name='weather')

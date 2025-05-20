from django.db import models
from utils.constants import SELECT_CITY

class City(models.Model):
    name = models.CharField(max_length=50, default="Bakı", choices=SELECT_CITY)

    def __str__(self):
        return self.name
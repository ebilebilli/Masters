from django.db import models
from cities_light.models import City as BaseCity

class City(models.Model):
    base_city = models.ForeignKey(BaseCity, on_delete=models.SET_NULL, null=True)

    @property
    def name(self):
        return self.base_city.name

    def __str__(self):
        return self.base_city.name
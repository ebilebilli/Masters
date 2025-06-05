from django.db import models
from django.contrib.auth import get_user_model

from .category_model import Category
from core.models.city_model import City


User = get_user_model()

class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    category = models.ManyToManyField(Category, related_name='services')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, related_name='services', null=True)

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):   
        return self.title
    

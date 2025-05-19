from django.db import models
from django.contrib.auth import get_user_model
from .category_model import Category


User = get_user_model()

class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    category = models.ManyToManyField(Category, related_name='services')

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):   
        return self.title
    
    #ok
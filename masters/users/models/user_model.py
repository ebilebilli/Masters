from django.db import models 
from django.contrib.auth.models import AbstractUser



# Muveqqeti User model (elaveler edilecek)
class User(AbstractUser):
    phone_number = models.CharField(max_length=13, unique=True)
    is_master = models.BooleanField()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'is_master', 'username']


    def __str__(self):
        return self.phone_number
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=60)  
    display_name = models.CharField(max_length=60)

    def __str__(self):
        return self.display_name
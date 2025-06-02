from django.db import models



class Language(models.Model):
    name = models.CharField(max_length=50, verbose_name="Dil adı")

    def __str__(self):
        return self.name
from django.db import models


class WorkImage(models.Model):
    image = models.ImageField(upload_to='work_images/', verbose_name="İş şəkli")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıra")

    def __str__(self):
        return f"İş Şəkli {self.image.url}"
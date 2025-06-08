from django.db import models


class WorkImage(models.Model):
    image = models.ImageField(upload_to='work_images/', verbose_name="İş şəkli")

    def __str__(self):
        try:
            return f"İş Şəkli {self.image.url}"
        except ValueError:
            return "İş Şəkli (fayl yoxdur)"

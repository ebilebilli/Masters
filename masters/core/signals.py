from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import City, District


@receiver(post_save, sender=City)
@receiver(post_delete, sender=City)
def clear_city_caches(sender, **kwargs):
    cache.delete('city_list')


@receiver(post_save, sender=District)
@receiver(post_delete, sender=District)
def clear_district_caches(sender, **kwargs):
    cache.delete('district_list')



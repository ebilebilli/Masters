from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models.user_model import CustomUser

@receiver(post_save, sender=CustomUser)
@receiver(post_delete, sender=CustomUser)
def clear_cache(sender, **kwargs):
    cache.delete_pattern('search_*') 
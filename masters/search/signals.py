from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models.user_model import CustomUser
from .documents import MasterDocument
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=CustomUser)
def update_master_document(sender, instance, created, **kwargs):
    try:
        master_doc = MasterDocument(
            meta={'id': instance.id},
            full_name=instance.full_name, 
            experience=instance.experience,
        )
        master_doc.save()
        logger.info(f"Master document updated/created for ID: {instance.id}")
    except Exception as e:
        logger.error(f"Error updating master document for ID {instance.id}: {str(e)}")


@receiver(post_delete, sender=CustomUser)
def delete_master_document(sender, instance, **kwargs):
    try:
        doc = MasterDocument.get(id=instance.id)
        doc.delete()
        logger.info(f"Master document deleted for ID: {instance.id}")
    except Exception as e:
        logger.error(f"Error deleting master document for ID {instance.id}: {str(e)}")
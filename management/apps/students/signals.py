from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Admission, FeeManagement


@receiver(post_save, sender=Admission)
def create_fee_management(sender, instance, created, **kwargs):
    if created:
        FeeManagement.objects.create(admission=instance)
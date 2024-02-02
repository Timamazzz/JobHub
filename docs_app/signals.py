# signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import EventImage, ExcursionImage, ApplicantAvatar
import os


@receiver(pre_save, sender=EventImage)
def set_event_preview(sender, instance, **kwargs):
    if not instance.original_name or not instance.extension:
        original_name = os.path.basename(instance.file.name)
        instance.original_name = original_name

        extension = os.path.splitext(original_name)[-1].lower()
        instance.extension = extension

    if instance.is_preview:
        EventImage.objects.filter(event=instance.event, is_preview=True).exclude(id=instance.id).update(
            is_preview=False)


@receiver(pre_save, sender=ExcursionImage)
def set_excursion_preview(sender, instance, **kwargs):
    if not instance.original_name or not instance.extension:
        original_name = os.path.basename(instance.file.name)
        instance.original_name = original_name

        extension = os.path.splitext(original_name)[-1].lower()
        instance.extension = extension

    if instance.is_preview:
        ExcursionImage.objects.filter(excursion=instance.excursion, is_preview=True).exclude(id=instance.id).update(
            is_preview=False)


@receiver(pre_save, sender=ApplicantAvatar)
def set_default_applicant_avatar(sender, instance, **kwargs):
    if not instance.original_name or not instance.extension:
        original_name = os.path.basename(instance.file.name)
        instance.original_name = original_name

        extension = os.path.splitext(original_name)[-1].lower()
        instance.extension = extension

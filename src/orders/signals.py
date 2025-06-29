# Django imports
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order
from .tasks import send_order_delivered_email


@receiver(post_save, sender=Order)
def notify_when_ready(sender, instance, created, **kwargs):
    if not created and instance.is_ready and not instance.is_notified:
        send_order_delivered_email.delay(instance.id)

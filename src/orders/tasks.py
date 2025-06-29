import logging

# Django imports
from django.db import transaction

from celery import shared_task
from celery.utils.log import get_task_logger

from .models import Order
from .utils import send_email

logger = get_task_logger(__name__)

@shared_task
def send_order_delivered_email(order_id):
    """
        Одноразова задача — відправити лист, коли замовлення позначене «готове».
        Викликається із view.
    """
    logger.info("Task started")
    order = Order.objects.filter(id=order_id, is_ready=True).first()
    if not order:
        return "Order not found or not ready"

    send_email(order)
    order.is_notified = True
    order.save()
    logger.info("Task completed successfully")
    return 'Email send'

@shared_task(bind=True)
def notify_single_order(order_id):
    """
    Відправляє e-mail про доставку для одного замовлення.
    Працює тільки, якщо is_ready=True та is_notified=False.
    """
    logger.info("Task started")
    with transaction.atomic():
        order = (Order.objects
                 .select_for_update(skip_locked=True)
                 .filter(id=order_id,
                         is_ready=True,
                         is_notified=False)
                 .first())

        if not order:
            return "Nothing to send"

    send_email(order)

    order.is_notified = True
    order.save(update_fields=["is_notified"])
    logger.info("Task completed successfully")
    return "Email sent"

@shared_task
def scan_and_notify_ready_orders():
    """
    Періодична Celery-Beat задача.
    Знаходить усі замовлення, які готові, але ще не повідомлені, і шле email.
    """
    queryset = Order.objects.filter(is_ready=True, is_notified=False)
    for order in queryset:
        notify_single_order.delay(order.id)

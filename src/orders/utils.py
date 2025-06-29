# Django imports
from django.core.mail import EmailMessage


def send_email(order):
    subject = f'Ваше замовлення №{order.id} готове!'
    body = (
        f"Дякуємо, {order.user.first_name or order.user.email}!\n\n"
        f"Замовлення №{order.id} готове.\n"
        f"Смачного! 🍽"
    )
    EmailMessage(subject, body, to=[order.user.email]).send()

# Django imports
from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.orders'

    def ready(self):
        import src.orders.signals

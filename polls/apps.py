# yourapp/apps.py
from django.apps import AppConfig

class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'  # o'z app nomingiz

    def ready(self):
        import polls.signals

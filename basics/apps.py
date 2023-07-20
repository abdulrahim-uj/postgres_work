from django.apps import AppConfig


class BasicsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'basics'

    def ready(self):
        from .functions import start_scheduler
        start_scheduler()

from django.apps import AppConfig


class NotificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notification'
    
    def ready(self):
        """Import signals when the app is ready."""
        import notification.signals

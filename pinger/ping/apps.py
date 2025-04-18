from django.apps import AppConfig


class PingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ping'

    def ready(self):
        super().ready()  # implement the default behavior
        import ping.signals

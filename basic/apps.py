from django.apps import AppConfig


class BasicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'basic'

    def ready(self):
        import basic.receivers
        super(BasicConfig, self).ready()

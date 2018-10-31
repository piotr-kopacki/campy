from django.apps import AppConfig


class CamappConfig(AppConfig):
    name = 'camapp'

    def ready(self):
        import camapp.signals

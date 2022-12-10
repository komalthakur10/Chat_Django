from django.apps import AppConfig


class ChatappConfig(AppConfig):
    name = 'chatapp'

    def ready(self):      # for signals.py
        import chatapp.signals

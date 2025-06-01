from django.apps import AppConfig

class TonAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monapp'  # adapte selon ton nom réel

    def ready(self):
        import monapp.signals  # Importez les signaux

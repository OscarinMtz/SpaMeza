from django.apps import AppConfig

class AppSpaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_spa'
    
    def ready(self):
        import app_spa.signals  # Registrar las señales
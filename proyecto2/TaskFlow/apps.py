from django.apps import AppConfig

class TaskflowConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TaskFlow'

    def ready(self):
        import TaskFlow.signals  # Esto activa los signals de la aplicación
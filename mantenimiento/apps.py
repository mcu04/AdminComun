from django.apps import AppConfig

class MantenimientoConfig(AppConfig):
    name = 'mantenimiento'

    def ready(self):
        import mantenimiento.signals
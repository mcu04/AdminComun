from celery import Celery
from celery.schedules import crontab

# Broker y backend usando Redis
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Ejemplo de schedule para Celery Beat (ejecuta la tarea cada día a las 8:00 AM)

CELERY_BEAT_SCHEDULE = {
    'enviar_recordatorios_diarios': {
        'task': 'mantenimiento.tasks.enviar_recordatorios',
        'schedule': crontab(hour=8, minute=0),  # cada día a las 08:00 AM
    },
}
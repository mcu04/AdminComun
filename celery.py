import os
from celery import Celery

# Establece la variable de entorno para el settings de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Documentacion_PostgreSQL.settings')

app = Celery('Documentacion_PostgreSQL')

# Carga la configuración desde settings.py, usando el prefijo CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubre tareas en todas las apps registradas
app.autodiscover_tasks()

# Ejemplo de tarea de depuración
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MantencionPreventiva, MaintenanceTask

@receiver(post_save, sender=MantencionPreventiva)
def create_or_update_maintenance_task(sender, instance, created, **kwargs):
    """
    Cada vez que se crea o actualiza una MantencionPreventiva,
    se crea o actualiza la tarea asociada en MaintenanceTask.
    Evita la creación duplicada de tareas de mantenimiento.
    """
    # Define el título de la tarea basado en el nombre de la mantención
    titulo = instance.instalacion if instance.instalacion else f"Mantención {instance.pk}"
    
    # Verifica si ya existe una tarea antes de crearla
    task, created_task = MaintenanceTask.objects.get_or_create(
        mantencion=instance,
        defaults={
            'titulo': titulo,
            'descripcion': instance.descripcion,
            'fecha_programada': instance.fecha_programada,
            'fecha_realizada': instance.fecha_realizada,
            'status': 'pendiente',
        }
    )
    
    if not created_task:  # Si ya existía, actualiza los datos
        task.titulo = titulo
        task.descripcion = instance.descripcion
        task.fecha_programada = instance.fecha_programada
        task.fecha_realizada = instance.fecha_realizada
        task.status = instance.status
        task.save()
    
    
    
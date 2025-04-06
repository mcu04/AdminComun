from django.db import models
from Aplicaciones.seguimientodocumentos.models import Comunidad  # Ajusta la importación según tu estructura
from django.contrib.auth import get_user_model
from datetime import date
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist



User = get_user_model()

def fecha_actual():
    return date.today()

# Modelo para las categorías de instalación 
class InstallationCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Instalación")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Categoría de Instalación"
        verbose_name_plural = "Categorías de Instalación"
        ordering = ['name']
        

    
# Modelo principal: Mantención Preventiva
STATUS_CHOICES = (
    ('pendiente', 'Pendiente'),
    ('revision', 'En Revisión'),
    ('proceso', 'En Proceso'),
    ('completado', 'Completado'),
)

# Opciones de periodo/frecuencia para la mantención
PERIODO_CHOICES = (
    ('semanal', 'Semanal'),
    ('quincenal', 'Quincenal'),
    ('mensual', 'Mensual'),
    ('trimestral', 'Trimestral'),
    ('semestral', 'Semestral'),
    ('anual', 'Anual'),
)


class MantencionPreventiva(models.Model):
    """
    Modelo principal para las mantenciones preventivas.
    Al guardarse (crear o actualizar), sincroniza su información con InstalacionPreventiva
    y crea o actualiza una tarea en el tablero Kanban (MaintenanceTask).
    """
    comunidad = models.ForeignKey('seguimientodocumentos.Comunidad', on_delete=models.CASCADE)
    category = models.ForeignKey(InstallationCategory, on_delete=models.SET_NULL, null=True, blank=True)
    custom_category = models.CharField(max_length=100, blank=True, null=True,
                                        help_text=_("Usa este campo si no se encuentra la categoría predefinida.")
    )
    instalacion = models.CharField(max_length=200)
    fecha_programada = models.DateField()
    fecha_realizada = models.DateField(blank=True, null=True)
    descripcion = models.TextField()
    observaciones = models.TextField(blank=True, null=True)
    # Campo de estado (Kanban)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendiente',
        help_text=_("Estado de la mantención en el tablero Kanban.")
    )
    
    # Campo de periodo/frecuencia
    periodo = models.CharField(
        max_length=20,
        choices=PERIODO_CHOICES,
        default='mensual',
        help_text=_("Frecuencia con la que se repite la mantención.")
    )
    # Otros campos, por ejemplo, costo, responsable, etc.
    responsable = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text=_("Ingrese el nombre del responsable de la mantención.")
    )
    costo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    
    def __str__(self):
        return f"Mantención de {self.instalacion} ({self.fecha_programada})"

    def save(self, *args, **kwargs):
        # Si se ingresa fecha realizada, forzamos el estado a "completado"
        if self.fecha_realizada:
            self.status = 'completado'
            
        is_new = self.pk is None  # Determina si es un registro nuevo
        
        # 1. Guarda la mantención preventiva
        super().save(*args, **kwargs)
        
        # 2. Sincroniza o crea la InstalacionPreventiva relacionada
        # (Se asume que el modelo InstalacionPreventiva tiene un ForeignKey a MantencionPreventiva
        #  con related_name="instalacion_preventiva" o similar)
        from .models import InstalacionPreventiva
    
        try:
            ip = self.instalacion_preventiva  # Se obtiene a través del related_name definido en InstalacionPreventiva
        except ObjectDoesNotExist:
            ip = InstalacionPreventiva(mantencion=self)
            
        # Actualizamos los campos relevantes del objeto relacionado.
        ip.instalacion = self.instalacion
        ip.fecha_instalacion = self.fecha_programada
        ip.descripcion = self.descripcion
        ip.observaciones = self.observaciones
        ip.responsable = self.responsable
        ip.costo = self.costo
        ip.save()
        
        # 3. Crear o actualizar la tarea en el tablero Kanban (MaintenanceTask)
        from .models import MaintenanceTask
        task_qs = MaintenanceTask.objects.filter(mantencion=self)
        if is_new and not task_qs.exists():
            MaintenanceTask.objects.create(
                mantencion=self,
                titulo=self.instalacion,
                descripcion=self.descripcion,
                fecha_programada=self.fecha_programada,
                fecha_realizada=self.fecha_realizada,
                status=self.status,
                responsable=self.responsable,
            )
            
        elif task_qs.exists():
            task = task_qs.first()
            task.titulo = self.instalacion
            task.descripcion = self.descripcion
            task.fecha_programada = self.fecha_programada
            task.fecha_realizada = self.fecha_realizada
            task.responsable = self.responsable
            task.status = self.status
            task.save()

    class Meta:
        verbose_name = _("Mantención Preventiva")
        verbose_name_plural = _("Mantenciones Preventivas")
        ordering = ['instalacion', 'fecha_programada']
            
        
    
# Modelo relacionado: Instalación Preventiva
class InstalacionPreventiva(models.Model):
    """
    Registra la información de la instalación preventiva sincronizada con la mantención.
    """
    mantencion = models.OneToOneField(
        'MantencionPreventiva',
        related_name='instalacion_preventiva',
        on_delete=models.CASCADE,
        help_text=_("Mantención preventiva asociada")
    )
    instalacion = models.CharField(
        max_length=200,
        blank=True,
        help_text=_("Nombre de la instalación. Se sincroniza con la mantención.")
    )
    fecha_instalacion = models.DateField(
        default=date.today,
        help_text=_("Fecha de la instalación preventiva (usualmente la fecha programada).")
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        help_text=_("Descripción de la mantención preventiva.")
    )
    observaciones = models.TextField(
        blank=True,
        null=True,
        help_text=_("Observaciones adicionales.")
    )
    responsable = models.CharField(
        max_length=200, 
        blank=True, 
        null=True, 
        help_text=_("Responsable de la mantención."))
    
    costo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_("Costo asociado a la mantención.")
    )
    
    def __str__(self):
        return f"Instalación Preventiva: {self.instalacion} ({self.fecha_instalacion})"
    
    class Meta:
        verbose_name = _("Instalación Preventiva")
        verbose_name_plural = _("Instalaciones Preventivas")

    
    #Tablero Kanban    
class MaintenanceTask(models.Model):
    """
    Modelo para las tareas de mantención mostradas en el tablero Kanban.
    Cada tarea está vinculada a una mantención preventiva y posee un estado que indica su progreso.
    """
    class StatusChoices(models.TextChoices):
        PENDIENTE = 'pendiente', _('Pendiente')
        REVISION = 'revision', _('En Revisión')
        PROCESO = 'proceso', _('En Proceso')
        COMPLETADO = 'completado', _('Completado')
        
    mantencion = models.ForeignKey('MantencionPreventiva', on_delete=models.CASCADE, related_name='tasks')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    fecha_programada = models.DateField(default=date.today)
    fecha_realizada = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDIENTE)
    responsable = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} ({self.get_status_display()})"
    
    @property
    def periodo(self):
        """
        Devuelve el periodo/frecuencia asociado a la mantención preventiva.
        """
        return self.mantencion.periodo
    
    class Meta:
        verbose_name = _("Tarea de Mantenimiento")
        verbose_name_plural = _("Tareas de Mantenimiento")
        ordering = ['fecha_programada']
    
class Mantenimiento(models.Model):
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    descripcion = models.TextField()
    STATUS_CHOICES = (
    ('pendiente', 'Pendiente'),
    ('revision', 'En Revisión'),
    ('proceso', 'En Proceso'),
    ('completado', 'Completado'),
)

    estado = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default='pendiente',
    help_text=_("Estado del mantenimiento.")
)

    def __str__(self):
        return f"Mantenimiento {self.descripcion} desde {self.fecha_inicio} hasta {self.fecha_fin}"

    def iniciar_mantenimiento(self):
        """Inicia el mantenimiento y notifica a los usuarios."""
        self.estado = 'en_curso'
        self.save()

        # Llamar a la función de notificación para informar a los usuarios
        from .views import send_maintenance_notification
        send_maintenance_notification(self.descripcion, self.fecha_inicio, self.fecha_fin)

    def finalizar_mantenimiento(self):
        """Finaliza el mantenimiento y notifica a los usuarios."""
        self.estado = 'finalizado'
        self.save()

        # Llamar a la función de notificación para informar a los usuarios
        from .views import send_maintenance_notification
        send_maintenance_notification(self.descripcion, self.fecha_inicio, self.fecha_fin, finalizado=True)
    
        
 

    
    






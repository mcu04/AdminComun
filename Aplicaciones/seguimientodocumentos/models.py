from django.db import models
from django.utils.timezone import now

# Clase para Documentacion
class documentacion(models.Model):
    tipo = models.CharField(max_length=100, verbose_name='Tipo')
    categoria = models.CharField(max_length=100, verbose_name='Categoría')
    titulo_documento = models.CharField(max_length=200, verbose_name='Título del Documento')

    def __str__(self):
        return f"{self.tipo}, {self.categoria}, {self.titulo_documento}"

    class Meta:
        verbose_name = 'Documentación'
        verbose_name_plural = 'Documentaciones'
        db_table = 'documentacion'
        ordering = ['tipo', 'categoria', 'titulo_documento']


# Clase para Seguimiento
class seguimiento(models.Model):
    EXISTE_CHOICES = [
        ('Si', 'Sí Existe'),
        ('No', 'No Existe')
    ]

    documentacion = models.ForeignKey(
        documentacion, null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='seguimientos',
        verbose_name='Documentación relacionada'
    )
    existe = models.CharField(
        max_length=10, choices=EXISTE_CHOICES, default='No',
        verbose_name='¿Existe el documento?'
    )
    fecha_registrado = models.DateField(
        auto_now_add=True, verbose_name='Fecha Registrado'
    )
    fecha_actualizado = models.DateField(
        null=True, blank=True, verbose_name='Fecha Actualizado'
    )
    observaciones = models.CharField(
        max_length=200, null=True, blank=True,
        verbose_name='Observaciones'
    )
    tipo = models.CharField(max_length=100, blank=True, null=True)
    categoria = models.CharField(max_length=100, blank=True, null=True, default="Sin Categoría")
    titulo_documento = models.CharField(max_length=255,blank=True, null=True, default="Sin Titulo")
    
    # Método personalizado para representar el seguimiento
    def seguimiento_documentacion(self):
        titulo = self.documentacion.titulo_documento if self.documentacion else "Sin Título"
        return (
            f"Título: {titulo}, Existe: {self.existe}, "
            f"Registrado: {self.fecha_registrado}, Actualizado: {self.fecha_actualizado}, "
            f"Observaciones: {self.observaciones}"
        )

    # Sobrescribir save para gestionar fechas
    def save(self, *args, **kwargs):
        if not self.pk:  # Si es una nueva instancia
            self.fecha_registrado = now().date()
        else:  # Actualización
            self.fecha_actualizado = now().date()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.seguimiento_documentacion()

    class Meta:
        verbose_name = 'Seguimiento'
        verbose_name_plural = 'Seguimientos'
        db_table = 'seguimiento'
        ordering = ['-fecha_actualizado']

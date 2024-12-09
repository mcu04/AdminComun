from django.db import models
from .choices import existe
from django.utils.timezone import now

# Create your models here.

class documentacion(models.Model):
    tipo = models.CharField(max_length=100, verbose_name='Tipo')
    categoria= models.CharField(max_length=100, verbose_name='Categoria')
    titulo_documento = models.CharField(max_length=200, verbose_name='Titulo del Documento')
    
    def base_documentacion(self):
        return f"{self.tipo}, {self.categoria}, {self.titulo_documento}"
    
    def __str__(self):
        return self.base_documentacion()  
    
    class Meta:
        verbose_name = 'Documentación'
        verbose_name_plural = 'Documentaciones'
        db_table = 'documentacion'
        ordering = ['tipo', 'categoria', 'titulo_documento']

class seguimiento(models.Model):
    EXISTE_CHOICES = [('Si', 'Sí Existe'), ('No', 'No Existe')]
    
    existe = models.CharField(max_length=10, choices=EXISTE_CHOICES, default='No', verbose_name='¿Existe el documento?')
    fecha_registrado = models.DateField(auto_now_add=True, verbose_name='Fecha Registrado')
    fecha_actualizado = models.DateField(null=True, blank=True, verbose_name='Fecha Actualizado')
    observaciones = models.CharField(max_length=200, null=True, blank=True, verbose_name='Observaciones')
    documentacion=models.ForeignKey('Documentacion', null=True, blank=True, on_delete=models.CASCADE, related_name='seguimientos', verbose_name='Documentación relacionada')
    
    def seguimiento_documentacion(self):

            titulo = self.documentacion.titulo_documento if self.documentacion else "Sin Título"
            return f"{titulo}, Registrado: {self.fecha_registrado}, Actualizado: {self.fecha_actualizado}, Observaciones: {self.observaciones}"
    def save(self, *args, **kwargs):
        """
        Lógica para manejo de fechas al guardar.
        """
        if not self.pk:  # Si es una nueva instancia
            self.fecha_registrado = now().date()  # Fecha de registro al crear
        
        else:  # Si es una actualización
            self.fecha_actualizado = now().date()  # Fecha de actualización
        super().save(*args, **kwargs)    # Llama al método save original
        
        
    def __str__(self):
        return self.seguimiento_documentacion()
    
    class Meta:
        verbose_name = 'Seguimiento'
        verbose_name_plural = 'Seguimientos'
        db_table = 'seguimiento'
        ordering = ['-fecha_actualizado']
        
    
        
    

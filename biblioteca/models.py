from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os


class Documento(models.Model):
    comunidad = models.ForeignKey('seguimientodocumentos.Comunidad', on_delete=models.CASCADE, related_name='biblioteca_documentos', null=True, blank=True)
    TIPO_CHOICES = [
        ('interno', 'Interno'),
        ('externo', 'Externo'),
    ]

    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    archivo = models.FileField(upload_to='biblioteca/', blank=True, null=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='interno')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    url_origen = models.URLField(blank=True, null=True)  # Para descargas externas
    # Nuevos campos
    
    estado = models.CharField(
        max_length=50,
        choices=[
            ('pendiente', 'Pendiente'),
            ('exitoso', 'Exitoso'),
            ('fallido', 'Fallido'),
        ],
        default='pendiente',
    )
    fecha_descarga = models.DateTimeField(blank=True, null=True)  # Fecha de última descarga

def __str__(self):
        return self.titulo
    
class Archivo(models.Model):
    TIPO_CHOICES = [
        ('Administracion', 'Administracion'),
        ('Contabilidad', 'Contabilidad'),
        ('Legal', 'Legal'),
        ('Mantenimiento', 'Mantenimiento'),
        ('Personal', 'Personal'),
        ('Prevencion de Riesgos', 'Prevencion de Riesgos'),
        ('Seguridad', 'Seguridad'),
        ('Otros', 'Otros'),
    ]

    CATEGORIA_CHOICES = [
        ('Comunicacion', 'Comunicacion'),
        ('Comunidad', 'Comunidad'),
        ('Contable', 'Contable'),
        ('Gastos Comunes', 'Gastos Comunes'),
        ('Gestion de Emergencia', 'Gestion de Emergencia'),
        ('Inmobiliaria', 'Inmobiliaria'),
        ('Leyes Laborales', 'Leyes Laborales'),
        ('Libros', 'Libros'),
        ('Mantenimiento Preventivo', 'Mantenimiento Preventivo'),
        ('Planos', 'Planos'),
        ('Proveedores', 'Proveedores'),
        ('Reglamentos', 'Reglamentos'),
        ('Resolucion de Conflictos', 'Resolucion de Conflictos'),
        ('Temas de Seguridad', 'Temas de Seguridad'),
        ('Otros', 'Otros'),
    ]
   
    comunidad = models.ForeignKey(
        'seguimientodocumentos.Comunidad',
        on_delete=models.CASCADE,
        related_name='archivos_biblioteca',
        null=True,
        blank=True
    )
    tipo = models.CharField(max_length=100, blank=True, null=True, choices=TIPO_CHOICES)
    categoria = models.CharField(max_length=100, blank=True, null=True, choices=CATEGORIA_CHOICES)
    titulo_documento = models.CharField(max_length=255)
    documento = models.FileField(upload_to='archivos/', blank=True, null=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo_documento
    
    def save(self, *args, **kwargs):
        if not self.documento:
            raise ValidationError("El archivo no puede estar vacío.")
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.documento:
            if os.path.isfile(self.documento.path):
                os.remove(self.documento.path)
        super().delete(*args, **kwargs)
    
    class Meta:
        ordering = ['tipo']  # Ordena por defecto de A-Z
        
    
    
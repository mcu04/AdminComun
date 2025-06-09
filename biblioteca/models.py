# biblioteca/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os

class TipoDocumento(models.Model):
    """
    Representa un “Tipo” general de archivo (Administración, Contabilidad, Legal, ...)
    """
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de Documento"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class CategoriaDocumento(models.Model):
    """
    Una Categoría específica, vinculada a un TipoDocumento.
    Ejemplo: “Reglamentos”, “Actas”, “Libros Contables”, etc.
    """
    tipo = models.ForeignKey(
        TipoDocumento,
        on_delete=models.CASCADE,
        related_name='categorias'
    )
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Categoría de Documento"
        verbose_name_plural = "Categorías de Documento"
        unique_together = ('tipo', 'nombre')
        ordering = ['tipo__nombre', 'nombre']

    def __str__(self):
        return self.nombre

class Archivo(models.Model):
    """
    Contiene la información de cada archivo (documento) en la biblioteca.
    En lugar de usar dos ChoiceFields planos, hacía “tipo” y “categoria”,
    ahora apuntamos a los modelos TipoDocumento y CategoriaDocumento.
    """

    comunidad = models.ForeignKey(
        'seguimientodocumentos.Comunidad',
        on_delete=models.CASCADE,
        related_name='archivos_biblioteca',
    )
    tipo = models.ForeignKey(
        TipoDocumento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='archivos'
    )
    categoria = models.ForeignKey(
        CategoriaDocumento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='archivos'
    )
    titulo_documento = models.CharField(max_length=255)
    documento = models.FileField(upload_to='archivos/', blank=True, null=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo_documento
    
    def save(self, *args, **kwargs):
        # 1) Validación: si hay categoría Y hay tipo, asegurar que
        #    esa categoría pertenece realmente a ese tipo.
        if self.categoria and self.tipo:
            if self.categoria.tipo_id != self.tipo_id:
                raise ValidationError("La categoría seleccionada no corresponde con el Tipo elegido.")

        # 2) Validación: comprobar que se envió un archivo con nombre válido.
        #    Un FileField recién creado sin subida real puede tener 'documento'
        #    como un FieldFile "vacío" (boolean False), o su atributo .name puede ser None/"". 
        if not self.documento or not getattr(self.documento, 'name', None):
            raise ValidationError("El archivo no puede estar vacío.")

        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Al eliminar el registro, también borramos el fichero del disco.
        if self.documento:
            if os.path.isfile(self.documento.path):
                os.remove(self.documento.path)
        super().delete(*args, **kwargs)
    
    class Meta:
        ordering = ['tipo__nombre', 'categoria__nombre', 'titulo_documento']
        
    
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
    

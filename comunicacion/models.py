from django.db import models
from django.contrib.auth.models import User
from Aplicaciones.seguimientodocumentos.models import Comunidad  # Importar el modelo correcto

class Residente(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre del Residente")
    correo = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE, related_name='residentes')

    def __str__(self):
        return self.nombre
    
class CorreoAdjunto(models.Model):
    archivo = models.FileField(upload_to='adjuntos/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.archivo.name

class Archivo(models.Model):
    archivo = models.FileField(upload_to='adjuntos/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.archivo.name
    
class Destinatario(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="destinatarios",
        verbose_name="Usuario",
        
    )
    
    nombre = models.CharField(max_length=255, verbose_name="Nombre")
    apellido = models.CharField(max_length=255, verbose_name="Apellido", default="") 
    correo = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    comunidad = models.ForeignKey(
        Comunidad,
        on_delete=models.CASCADE,
        related_name='destinatarios',
        verbose_name="Comunidad"
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido} <{self.correo}>"
    
    class Meta:
        verbose_name = "Destinatario"
        verbose_name_plural = "Destinatarios"
        ordering = ['nombre', 'apellido']
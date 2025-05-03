from django.db import models
from django.utils.timezone import now
from django.views.generic import ListView
from django import forms
from django.apps import apps
from django.contrib.auth.models import AbstractUser
from django.conf import settings  # Acceso global al AUTH_USER_MODEL
from django.contrib.auth.models import User 


# Clase para Documentacion
class Documentacion(models.Model):
    tipo = models.CharField(max_length=100, verbose_name='Tipo')
    categoria = models.CharField(max_length=100, verbose_name='Categoría')
    titulo_documento = models.CharField(max_length=200, verbose_name='Título del Documento')
    comunidad = models.ForeignKey('Comunidad',default=None, null=True, on_delete=models.CASCADE, related_name='seguimiento_documentos', verbose_name='Comunidad')
    
    def __str__(self):
        # Define cómo se verá cada instancia en el formulario
        return f"{self.tipo} - {self.categoria} - {self.titulo_documento}"


    class Meta:
        verbose_name = 'Documentación'
        verbose_name_plural = 'Documentaciones'
        db_table = 'seguimientodocumentos_Documentacion'
        ordering = ['tipo', 'categoria', 'titulo_documento']


# Clase para Seguimiento
class Seguimiento(models.Model):
    EXISTE_CHOICES = [
        ('Si', 'Si Existe'),
        ('No', 'No Existe')
    ]
    
    documentacion = models.ForeignKey(
        'Documentacion', null=True, blank=True,    # Referencia directa al modelo Documentacion
        on_delete=models.CASCADE,
        related_name='seguimientos',
        verbose_name='Documentación relacionada'
    )
    existe = models.CharField(
        max_length=2, choices=EXISTE_CHOICES, default='No',
        verbose_name='¿Existe el documento?'
    )
    fecha_registrado = models.DateField(editable=False, 
        null=True, blank=True, auto_now_add=True, verbose_name='Fecha Registrado'
    )
    fecha_actualizado = models.DateField(editable=False,
        null=True, blank=True, verbose_name='Fecha Actualizado'
    )
    observaciones = models.CharField(
        max_length=200, null=True, blank=True,
        verbose_name='Observaciones'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True,
        verbose_name='Usuario asociado'
        )  # Relación con el usuario
    comunidad = models.ForeignKey(
        'Comunidad', on_delete=models.CASCADE,
        verbose_name='seguimientos'
        )
    
        # Método personalizado para representar el seguimiento
    def seguimiento_documentacion(self):
        #Representa el seguimiento como una cadena legible.
        titulo = self.documentacion.titulo_documento if self.documentacion else "Sin Título"
        return (
            f"Título: {titulo}, Existe: {self.existe}, "
            f"Registrado: {self.fecha_registrado}, "
            f"Actualizado: {self.fecha_actualizado}, Observaciones: {self.observaciones}"
        )
        
        #Sobrescribe el método save para gestionar fechas y estados.
    def save(self, *args, **kwargs):
        if not self.pk:  # Si es una nueva instancia
            self.fecha_registrado = now().date()
        elif self.existe == 'Si':
            self.fecha_actualizado = now().date()  # Actualiza la fecha si existe el documento
                
        # Llamar al método original de guardado       
        super(Seguimiento, self).save(*args, **kwargs)
                        
        #Representa el seguimiento de manera clara y legible.
    def __str__(self):
        titulo = self.documentacion.titulo_documento if self.documentacion else "Sin Título"
        return f"{titulo} - Existe: {self.existe}"

    class Meta:
        verbose_name = 'Seguimiento'
        verbose_name_plural = 'Seguimientos'
        db_table = 'Seguimiento'
        ordering = ['-fecha_actualizado']
        
class Comunidad(models.Model):
        nombre = models.CharField(max_length=100, verbose_name="Nombre de la Comunidad", unique=True)
        direccion = models.CharField(max_length=200, verbose_name="Dirección")
        descripcion = models.TextField(blank=True, null=True,verbose_name="Descripción")
        usuarios = models.ManyToManyField(User, related_name='comunidades_seguimiento')
        administrador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comunidades_administradas',
        verbose_name="Administrador"
        )
        
class Meta:
        verbose_name = 'Comunidad'
        verbose_name_plural = 'Comunidades'
        ordering = ['nombre']  # Ordena por nombre alfabéticamente
        constraints = [
            models.UniqueConstraint(fields=['nombre', 'direccion'], name='unique_comunidad_direccion')
        ]  # Restricción única en lugar de unique_together

def __str__(self):
    return self.nombre
    
def get_documentos(self):
    """ Obtiene los documentos asociados a esta comunidad."""
    
    Documentacion = apps.get_model('seguimientodocumentos', 'Documentacion') 
    return Documentacion.objects.filter(comunidad=self)




class BibliotecaArchivo(models.Model):
    tipo = models.CharField(max_length=100, blank=True, null=True)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    titulo_documento = models.CharField(max_length=255)
    documento = models.CharField(max_length=100)
    fecha_subida = models.DateTimeField()
    comunidad = models.ForeignKey('Comunidad', on_delete=models.CASCADE)

    class Meta:
        db_table = 'biblioteca_biblioteca_archivo'


class BibliotecaDocumento(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    archivo = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=10)
    fecha_subida = models.DateTimeField()
    estado = models.CharField(max_length=50)
    fecha_descarga = models.DateTimeField(blank=True, null=True)
    url_origen = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'biblioteca_biblioteca_documento'


class DocumentacionForm(forms.ModelForm):
    class Meta:
        model = Documentacion
        fields = ['tipo', 'categoria', 'titulo_documento', 'comunidad']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtener el usuario
        super().__init__(*args, **kwargs)
        if user:
            self.fields['comunidad'].queryset = Comunidad.objects.filter(administrador=user)
            
            

        
        






        







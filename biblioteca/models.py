from django.db import models

class Documento(models.Model):
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
    tipo = models.CharField(max_length=100, blank=True, null=True, choices=TIPO_CHOICES)
    categoria = models.CharField(max_length=100, blank=True, null=True, choices=CATEGORIA_CHOICES)
    titulo_documento = models.CharField(max_length=255)
    documento = models.FileField(upload_to='archivos/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo_documento
    
    class Meta:
        ordering = ['tipo']  # Ordena por defecto de A-Z

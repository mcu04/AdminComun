from django.db import models
from Aplicaciones.seguimientodocumentos.models import Comunidad  # Ajusta la importación según tu estructura

class MantencionPreventiva(models.Model):
    instalacion = models.CharField(max_length=100)
    fecha = models.DateField()
    descripcion = models.TextField()
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE, default=1, related_name='mantenciones')

    def __str__(self):
        return f"{self.instalacion} - {self.fecha}"

class ContratoMantenimiento(models.Model):
    instalacion = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100)
    contrato = models.CharField(max_length=50)
    contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    valor_servicio = models.CharField(max_length=50)  # Por ejemplo, en UF
    periodo = models.CharField(max_length=20)  # e.g., ANUAL, BIANUAL, etc.
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE, default=1, related_name='contratos')

    def __str__(self):
        return f"{self.instalacion} - {self.empresa}"

class ReparacionGeneral(models.Model):
    area = models.CharField(max_length=100)
    problema = models.TextField()
    estado = models.CharField(
        max_length=20, 
        choices=[('Pendiente', 'Pendiente'), ('En Proceso', 'En Proceso'), ('Resuelto', 'Resuelto')]
    )
    fecha_solicitud = models.DateField(auto_now_add=True)
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE, default=1, related_name='reparaciones')

    def __str__(self):
        return f"{self.area} - {self.estado}"

class CotizacionProveedor(models.Model):
    proveedor = models.CharField(max_length=100)
    servicio = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE, default=1, related_name='cotizaciones')

    def __str__(self):
        return f"{self.proveedor} - {self.servicio}"

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    servicios = models.TextField(help_text="Lista de servicios separados por comas.")
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE, default=1, related_name='proveedores')

    def __str__(self):
        return self.nombre

from django.contrib import admin
from Aplicaciones.seguimientodocumentos.models import Documentacion,Seguimiento
# Register your models here.

# Configuración para el modelo 'seguimiento'
class seguimientoAdmin(admin.ModelAdmin):
    readonly_fields = ('fecha_registrado', 'fecha_actualizado')  # Campos de solo lectura
    list_display = ('id', 'existe', 'fecha_registrado', 'fecha_actualizado', 'observaciones')  # Campos mostrados en la lista
    list_filter = ('existe',)  # Filtro para facilitar la búsqueda por estado de existencia
    search_fields = ('observaciones',)  # Habilitar búsqueda por campo de observaciones
    fieldsets = (  # Organización de los campos en secciones
        (None, {
            'fields': ('existe', 'documentacion', 'observaciones'),
        }),
        ('Fechas', {
            'fields': ('fecha_registrado', 'fecha_actualizado'),
        }),
    )
        
# Configuración para el modelo 'documentacion'
class documentacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo_documento', 'tipo', 'categoria')  # Campos mostrados en la lista
    search_fields = ('titulo_documento', 'tipo', 'categoria')  # Habilitar búsqueda por título, tipo y categoría
    ordering = ('tipo', 'categoria')  # Orden por tipo y categoría
    fields = ('tipo', 'categoria', 'titulo_documento')  # Mostrar solo estos campos en la vista de edición

# Registrar los modelos en el panel de administración
admin.site.register(Documentacion, documentacionAdmin)  # Registrar 'documentacion' con configuración personalizada
admin.site.register(Seguimiento, seguimientoAdmin)  # Registrar 'seguimiento' con configuración personalizada
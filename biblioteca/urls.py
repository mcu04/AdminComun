from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'biblioteca'   # Importante para que los links funcionen

urlpatterns = [
    # 1) Landing (opcional)
    path('', views.home, name='home'),  
    # ————— Listado de archivos de una comunidad —————
    # URL definitiva: biblioteca/<comunidad_id>/archivos/
    path('biblioteca/<int:comunidad_id>/archivos/', views.biblioteca_archivos, 
        name='biblioteca_archivos'),
    # ————— Subir nuevo archivo —————
    # URL definitiva: biblioteca/<comunidad_id>/subir/
    path('biblioteca/<int:comunidad_id>/subir/', views.subir_archivo, name='subir_archivo'),
    # ————— Descargar un archivo —————
    # URL definitiva única: archivos/<archivo_id>/descargar/
    path('archivos/<int:archivo_id>/descargar/',views.descargar_archivo,         name='descargar_archivo'),
    
    # ————— Eliminar un archivo —————
    path('eliminar/<int:archivo_id>/', views.eliminar_archivo, name='eliminar_archivo'),
    # ————— (Opcional) Descarga desde URL externa —————
    #path('biblioteca/descargar-externo/<path:url>/', descargar_archivo_externo, name='descargar_externo'),
    # ————— Contacto u otras vistas auxiliares —————
    path('contacto/', views.contacto, name='contacto'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



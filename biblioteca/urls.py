from django.urls import path
from . import views
from .views import descargar_archivo_externo
from django.conf import settings
from django.conf.urls.static import static

app_name = 'biblioteca'   # Importante para que los links funcionen

urlpatterns = [
    path('', views.home, name='home'),  # Ruta para la vista 'home'
    path('lista', views.biblioteca_lista, name='biblioteca_lista'),
    path('biblioteca/', views.biblioteca_view, name='biblioteca'),   # Para la vista de la biblioteca
    path('<int:pk>/', views.biblioteca_detalle, name='biblioteca_detalle'),
    path('biblioteca/descargar/<int:id>/', views.descargar_archivo, name='descargar_archivo'),  # Para descargar archivos
    path('biblioteca/archivos/<int:comunidad_id>', views.biblioteca_archivos, name='biblioteca_archivos'),
    path('biblioteca/subir/', views.subir_archivo, name='subir_archivo'),  # Para subir archivos
    path('biblioteca/<int:comunidad_id>/subir/', views.subir_archivo, name='subir_archivo'),
    path('descargar_externo/<str:url>/', descargar_archivo_externo, name='descargar_externo'),
    path('eliminar/<int:archivo_id>/', views.eliminar_archivo, name='eliminar_archivo'),
    path('contacto/', views.contacto, name='contacto'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



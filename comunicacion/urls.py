from django.urls import path
from . import views
from .views import index, contacto, obtener_destinatarios
from .views import subir_archivos, enviar_correo
from .views import enviar_correo_individual, enviar_correo_masivo
from .views import (
    DestinatarioListView,
    DestinatarioCreateView,
    DestinatarioUpdateView,
    DestinatarioDeleteView,
    gestionar_destinatarios,)

app_name = 'comunicacion'  # Asegura que usas el namespace 'comunicacion'

urlpatterns = [
    path('',index, name='index'),    # Correo Individual
    path('contacto/',contacto, name='contacto'),
    path('subir-archivos/', subir_archivos, name='subir_archivos'),
    path('enviar-correo/', enviar_correo, name='enviar_correo'),
    path('correo-individual/<int:comunidad_id>/', enviar_correo_individual, name='enviar_correo_individual'),
    path('correo-masivo/<int:comunidad_id>/', enviar_correo_masivo, name='enviar_correo_masivo'),
    path("destinatarios/", gestionar_destinatarios, name="gestionar_destinatarios"),
    #path("destinatarios/nuevo/", DestinatarioCreateView.as_view(), name="destinatario_create"),
    path("destinatarios/<int:pk>/editar/", DestinatarioUpdateView.as_view(), name="destinatario_update"),
    path("destinatarios/<int:pk>/eliminar/", DestinatarioDeleteView.as_view(), name="destinatario_delete"),
    path('obtener-destinatarios/', obtener_destinatarios, name='obtener_destinatarios'),
    # O puedes usar la vista funcional:
    path("destinatarios/nuevo/", gestionar_destinatarios, name="destinatario_create"),
]
    



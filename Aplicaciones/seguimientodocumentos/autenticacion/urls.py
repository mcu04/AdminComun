# autenticacion/urls.py
from django.urls import path
from . import views  # Importa tus vistas personalizadas
from Aplicaciones.seguimientodocumentos.autenticacion import views
from .views import cerrar_sesion

app_name = 'autenticacion'

urlpatterns = [
    # Vista personalizada para iniciar sesión
    path('iniciar-sesion/', views.iniciar_sesion, name='iniciar_sesion'),

    # Vista personalizada para cerrar sesión
    path("cerrar_sesion/", cerrar_sesion, name="cerrar_sesion"),
    path('terminos-condiciones/', views.terminos_condiciones, name='terminos_condiciones'),

    # Recuperación de contraseña personalizada
    path("password_reset/", views.password_reset_request, name="password_reset_request"),
    path("reset/<uuid:token>/", views.password_reset_confirm, name="password_reset_confirm"),
]





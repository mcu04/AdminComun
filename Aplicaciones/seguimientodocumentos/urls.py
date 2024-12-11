from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import exportar_excel
from .views import exportar_pdf


app_name = "seguimientodocumentos"    # Importante para que los links funcionen
urlpatterns = [
    path('listar/', views.listar_seguimiento, name='listar_seguimiento'),
    path("crear/", views.crear_seguimiento, name="crear_seguimiento"),
    path("pendiente/", views.seguimiento_pendiente, name="seguimiento_pendiente"),
    path("<int:seguimiento_id>/", views.detallesseguimiento, name="detalle_seguimiento"),
    path("<int:id>/eliminar/", views.eliminar_seguimiento, name="eliminar_seguimiento"),
    path("cerrar-sesion/", views.cerrar_sesion, name="cerrar_sesion"),  # Cambia espacios por guiones medios o bajos
    path("iniciar-sesion/", views.iniciar_sesion, name="iniciar_sesion"),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('pagina_inicio', views.pagina_inicio, name='pagina_inicio'),
    path('pagina_principal', views.pagina_principal, name='pagina_principal'),  # Ahora la raíz apunta a esta vista
    path('exportar-excel/', views.exportar_excel, name='exportar_excel'),
    path('exportar-pdf/', exportar_pdf, name='exportar_pdf'),
]


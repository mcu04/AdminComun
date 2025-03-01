from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import exportar_excel
from .views import exportar_pdf
from .views import DocumentacionListView, documentacion_create
from .views import documentacion_edit, documentacion_delete
from django.contrib.auth.views import LoginView
from .views import PasswordResetConfirmView
from .views import (
    DocumentacionListView, documentacion_create, documentacion_edit, documentacion_delete
)

app_name = "seguimientodocumentos"    # Importante para que los links funcionen

urlpatterns = [
    path('seguimiento/listar/<int:comunidad_id>/', views.listar_seguimiento, name='listar_seguimiento'),    
    path('seguimiento/editar/<int:seguimiento_id>//', views.editar_seguimiento, name='editar_seguimiento'), 
    path("crear/<int:comunidad_id>/", views.crear_seguimiento, name="crear_seguimiento"),
    path('pendiente/<int:comunidad_id>/', views.seguimiento_pendientes, name='seguimiento_pendientes'),
    path("<int:seguimiento_id>/", views.detallesseguimiento, name="detalle_seguimiento"),
    path('seguimiento/eliminar/<int:seguimiento_id>/', views.eliminar_seguimiento, name='eliminar_seguimiento'),
    path("cerrar-sesion/", views.cerrar_sesion, name="cerrar_sesion"),  # Cambia espacios por guiones medios o bajos
    path('iniciar-sesion/',views.iniciar_sesion, name='iniciar_sesion'),
    path('seguimiento/exportar/excel/<str:tipo_seguimiento>/<int:comunidad_id>/', views.exportar_excel, name='exportar_excel'),
    path('seguimiento/exportar/excel/actualizado/', views.exportar_excel, name='exportar_excel'),
    path('seguimiento/exportar/excel/pendiente/', views.exportar_excel, name='exportar_excel'),
    path('seguimiento/exportar/pdf/<str:tipo_seguimiento>/', views.exportar_pdf, name='exportar_pdf'),
    path('exportar/pdf/<str:tipo_seguimiento>/<int:comunidad_id>/', views.exportar_pdf, name='exportar_pdf'),
    path('seguimiento/password_reset/', auth_views.PasswordResetView.as_view(
        template_name='seguimientodocumentos/password_reset_form.html'
    ), name='password_reset'),
    path('seguimiento/password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='seguimientodocumentos/password_reset_done.html'
    ), name='password_reset_done'),
    path('seguimiento/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='seguimientodocumentos/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('seguimiento/reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='seguimientodocumentos/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    path('pagina_inicio', views.pagina_inicio, name='pagina_inicio'),
    path('pagina_principal', views.pagina_principal, name='pagina_principal'),  # Ahora la raíz apunta a esta vista
    path('documentos/', DocumentacionListView.as_view(), name='documentos_list'),
    path('documentos/nuevo/', documentacion_create, name='documentacion_create'),
    path('documentos/<int:pk>/editar/', documentacion_edit, name='documentacion_edit'),
    path('documentos/<int:pk>/eliminar/', documentacion_delete, name='documentacion_delete'),
    path('documentacion/', views.documentacion_list, name='documentacion_list'),
    path('documentacion/crear/', views.documentacion_create, name='documentacion_create'),
    path('registrar-comunidad/', views.registrar_comunidad, name='registrar_comunidad'),
    path('comunidad/<int:comunidad_id>/', views.detalles_comunidad, name='comunidad'),
    path('comunidades/', views.listar_comunidades, name='comunidades'),
    path('comunidades/actualizar/<int:pk>/', views.actualizar_comunidad, name='actualizar_comunidad'),
    path('comunidades/eliminar/<int:pk>/', views.eliminar_comunidad, name='eliminar_comunidad'),


]

    

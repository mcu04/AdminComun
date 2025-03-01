from django.urls import path
from . import views

app_name = 'mantenimiento'

urlpatterns = [
    path('', views.MantenimientoDashboardView.as_view(), name='dashboard'),
    # Mantención Preventiva
    path('mantencion/<int:comunidad_id>/', views.MantencionPreventivaListView.as_view(), name='mantencion_list'),
    path('mantencion/nuevo/<int:comunidad_id>/', views.MantencionPreventivaCreateView.as_view(), name='mantencion_create'),
    # Contratos Empresas de Mantenimiento
    path('contratos/<int:comunidad_id>/', views.ContratoMantenimientoListView.as_view(), name='contrato_list'),
    path('contratos/nuevo/<int:comunidad_id>/', views.ContratoMantenimientoCreateView.as_view(), name='contrato_create'),
    # Reparaciones Generales
    path('reparaciones/<int:comunidad_id>/', views.ReparacionGeneralListView.as_view(), name='reparacion_list'),
    path('reparaciones/nuevo/<int:comunidad_id>/', views.ReparacionGeneralCreateView.as_view(), name='reparacion_create'),
    # Cotizaciones de Proveedores
    path('cotizaciones/<int:comunidad_id>/', views.CotizacionProveedorListView.as_view(), name='cotizacion_list'),
    path('cotizaciones/nuevo/<int:comunidad_id>/', views.CotizacionProveedorCreateView.as_view(), name='cotizacion_create'),
    # Proveedores en el Mercado
    path('proveedores/<int:comunidad_id>/', views.ProveedorListView.as_view(), name='proveedor_list'),
    path('proveedores/nuevo/<int:comunidad_id>/', views.ProveedorCreateView.as_view(), name='proveedor_create'),
]

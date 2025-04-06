from django.urls import path
from . import views
from .views import MantencionPreventivaListView, MantencionPreventivaCreateView, MantencionPreventivaUpdateView, MantencionPreventivaDeleteView
from .views import mantenciones_json, MantencionInformeView, KanbanBoardView
from .views import CalendarView, EventosMantenciones, calendario_mantenciones


app_name = 'mantenimiento'

urlpatterns = [
    path('dashboard/<int:comunidad_id>/', views.MantenimientoDashboardView.as_view(), name='dashboard'),
    # Mantención Preventiva
    path('mantencion_list/<int:comunidad_id>/', MantencionPreventivaListView.as_view(), name='mantencion_list'),
    path('mantencion/nuevo/<int:comunidad_id>/', MantencionPreventivaCreateView.as_view(), name='mantencion_create'),
    path("mantencion/editar/<int:comunidad_id>/<int:pk>/", MantencionPreventivaUpdateView.as_view(), name="mantencion_update"),
    path("mantencion/eliminar/<int:comunidad_id>/<int:pk>/", MantencionPreventivaDeleteView.as_view(), name="mantencion_delete"),
    
       
    path('mantenciones/json/<int:comunidad_id>/', mantenciones_json, name='mantenciones_json'),
    path('mantencion/informe/<int:comunidad_id>/', MantencionInformeView.as_view(), name='mantencion_informe'),
    path('kanban/<int:comunidad_id>/', KanbanBoardView.as_view(), name='kanban'),
    
    path('calendario/<int:comunidad_id>/', CalendarView.as_view(), name='calendario'),
    path('calendario/<int:comunidad_id>/', calendario_mantenciones, name='calendario_mantenciones'),
    # Endpoint que devuelve el JSON de mantenciones
    path('eventos/<int:comunidad_id>/', EventosMantenciones.as_view(), name='eventos_mantenciones'),
    
    
    
    
    
]

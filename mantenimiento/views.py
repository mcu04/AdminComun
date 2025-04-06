from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import (MantencionPreventiva)
from .forms import (MantencionPreventivaForm)
from .filters import MantencionPreventivaFilter
from django.views.generic import ListView
import django_filters
from django_filters.views import FilterView
from django.http import JsonResponse, HttpResponseRedirect
from Aplicaciones.seguimientodocumentos.models import Comunidad
import json
from django.core import serializers
from .models import MaintenanceTask
from django.views.decorators.csrf import csrf_exempt
from .models import InstalacionPreventiva
from django.db import IntegrityError
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View
import datetime
from .notifications import send_maintenance_notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Count, Q
from datetime import datetime
from .models import MantencionPreventiva
from django.http import Http404
from django.views.generic import ListView



# Mantención Preventiva
class MantencionPreventivaListView(ListView):
    model = MantencionPreventiva
    template_name = "mantenimiento/mantencion_list.html"
    context_object_name = "mantenciones"
    
    def get_queryset(self):

        # Obtiene la comunidad a partir del parámetro en la URL
        comunidad_id = self.kwargs.get('comunidad_id')
        comunidad = get_object_or_404(Comunidad, id=comunidad_id)
        qs = super().get_queryset().filter(comunidad=comunidad)
        
        # Obtén el filtro enviado como query parameter
        filtro = self.request.GET.get('filtro')
        if filtro == 'realizadas':
            qs = qs.filter(fecha_realizada__isnull=False)
        elif filtro == 'pendientes':
            qs = qs.filter(fecha_realizada__isnull=True)
        elif filtro == 'instalaciones_pendientes':
            # Para instalaciones pendientes, se agrupan (distinct) por el campo 'instalacion'
            qs = qs.filter(fecha_realizada__isnull=True).distinct('instalacion')
        
        # Ordena por fecha_programada (ascendente) y, en caso de igualdad, por instalacion (A-Z)
        qs = qs.order_by('fecha_programada', 'instalacion')
        return qs
    
    def get_context_data(self, **kwargs):
        
        """Agrega al contexto la instancia de la comunidad para usarla en la plantilla."""
        
        context = super().get_context_data(**kwargs)
        comunidad_id = self.kwargs.get('comunidad_id')
        comunidad = get_object_or_404(Comunidad, id=comunidad_id)
        context['comunidad'] = comunidad
        # Pasa el filtro actual para usarlo en la plantilla si lo necesitas
        context['filtro'] = self.request.GET.get('filtro', 'todas')
        return context

# Define el FilterSet para el modelo de mantenciones
class MantencionPreventivaFilter(django_filters.FilterSet):
    # Ejemplo: filtrar por fecha (a partir de una fecha)
    fecha = django_filters.DateFilter(lookup_expr='gte', label="Fecha desde")
    
    class Meta:
        model = MantencionPreventiva
        fields = ['instalacion', 'fecha'] 
        
class MantencionPreventivaCreateView(CreateView):
    model = MantencionPreventiva
    form_class = MantencionPreventivaForm
    template_name = "mantenimiento/mantencion_form.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comunidad = get_object_or_404(Comunidad, id=self.kwargs.get('comunidad_id'))
        context['comunidad'] = comunidad
        return context

    
    def form_valid(self, form):
        """
        Método que se ejecuta cuando el formulario es válido. 
        Asigna la comunidad desde la URL y el responsable desde el usuario autenticado.
        """
        # Asigna la comunidad según el parámetro de la URL.
        comunidad = get_object_or_404(Comunidad, id=self.kwargs['comunidad_id'])
        form.instance.comunidad = comunidad
        # Asigna automáticamente el responsable al usuario autenticado.
        form.instance.responsable = self.request.user.get_full_name() or self.request.user.username
        # Guarda la mantención preventiva; este llamado invoca el método save() del modelo,
        # que se encarga de crear/actualizar el registro relacionado en InstalacionPreventiva.
        self.object = form.save()
        messages.success(self.request, "Mantención preventiva creada con éxito.")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('mantenimiento:mantencion_list', kwargs={'comunidad_id': self.kwargs.get('comunidad_id')})
    
def eventos_mantenciones(request, comunidad_id):
    mantenciones = MantencionPreventiva.objects.filter(comunidad_id=comunidad_id)
    events = []
    for m in mantenciones:
        events.append({
            'title': m.instalacion,
            'start': m.fecha_programada.strftime('%Y-%m-%d'),
            'end': m.fecha_realizada.strftime('%Y-%m-%d') if m.fecha_realizada else m.fecha_programada.strftime('%Y-%m-%d'),
            'description': m.descripcion,
            # Puedes agregar colores según el estado, etc.
        })
    return JsonResponse(events, safe=False)


    
def mantenciones_json(request, comunidad_id):
    """
    Retorna un JSON con la lista de mantenciones preventivas para una comunidad específica,
    formateado para que DataTables pueda interpretarlo correctamente.
    
    La respuesta tiene la siguiente estructura:
    {
        "data": [
            {
                "instalacion": "Nombre de la instalación",
                "fecha_programada": "YYYY-MM-DD",
                "fecha_realizada": "YYYY-MM-DD" o "Pendiente",
                "descripcion": "Descripción de la mantención" o "Sin descripción",
                "observaciones": "Observaciones" o "Sin observaciones",
                "acciones": "<a href='...'>Editar</a> <a href='...'>Eliminar</a>"
            },
            ...
        ]
    }
    """
    
    comunidad = get_object_or_404(Comunidad, id=comunidad_id)
    # Filtra las mantenciones de la comunidad
    mantenciones = MantencionPreventiva.objects.filter(comunidad=comunidad).values(
        "id", "instalacion", "fecha_programada", "fecha_realizada", "descripcion", "observaciones"
)
    
    data = []
    for m in mantenciones:
        data.append({
            "instalacion": m.get("instalacion", ""),
            "fecha_programada": m["fecha_programada"].strftime("%Y-%m-%d") if m["fecha_programada"] else "",
            "fecha_realizada": m["fecha_realizada"].strftime("%Y-%m-%d") if m["fecha_realizada"] else "Pendiente",
            "descripcion": m.get("descripcion") or "Sin descripción",
            "observaciones": m.get("observaciones") or "Sin observaciones",
            "acciones": (
                f"<a href='/mantenimiento/editar/{m['id']}/' class='btn btn-sm btn-warning'>Editar</a> "
                f"<a href='/mantenimiento/eliminar/{m['id']}/' class='btn btn-sm btn-danger'>Eliminar</a>"
            )
        })
    
    return JsonResponse({"data": data})



def calendario_mantenciones(request, comunidad_id):
    """
    Vista para mostrar el Calendario de Mantenciones.
    """
    comunidad = get_object_or_404(Comunidad, id=comunidad_id)
    # (Opcional) Si quieres pasar las mantenciones al template, hazlo aquí.
    # Pero normalmente FullCalendar las consume vía AJAX (eventos_mantenciones).
    mantenciones = MantencionPreventiva.objects.filter(comunidad=comunidad)

    return render(
        request,
        "mantenimiento/calendario.html",
        {
            "comunidad": comunidad,
            "mantenciones": mantenciones,  # Opcional si lo usas en la plantilla
        }
    )

class MantencionPreventivaUpdateView(UpdateView):
    model = MantencionPreventiva
    form_class = MantencionPreventivaForm
    template_name = "mantenimiento/mantencion_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comunidad = get_object_or_404(Comunidad, id=self.kwargs.get('comunidad_id'))
        context.update({
            'comunidad': comunidad,
            'comunidad_id': comunidad.id,
        })
        return context

    def get_success_url(self):
        return reverse_lazy('mantenimiento:mantencion_list', kwargs={'comunidad_id': self.kwargs.get('comunidad_id')})
    
class MantencionPreventivaDeleteView(DeleteView):
    model = MantencionPreventiva
    template_name = "mantenimiento/mantencion_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy('mantenimiento:mantencion_list', kwargs={'comunidad_id': self.kwargs.get('comunidad_id')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comunidad_id = self.kwargs.get('comunidad_id')
        context['comunidad'] = get_object_or_404(Comunidad, id=comunidad_id)
        return context

class MantencionInformeView(TemplateView):
    template_name = "mantenimiento/mantencion_informe.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comunidad_id = self.kwargs.get('comunidad_id')
        # Aseguramos que la comunidad existe y la pasamos al contexto
        comunidad = get_object_or_404(Comunidad, id=comunidad_id)
        context['comunidad'] = comunidad
        
        # Leer los parámetros GET
        year = self.request.GET.get('year')
        month = self.request.GET.get('month')
        
        # Consulta inicial: todas las mantenciones de la comunidad
        queryset = MantencionPreventiva.objects.filter(comunidad=comunidad)
        
        # Filtrar por año si se especifica
        if year:
            queryset = queryset.filter(fecha_programada__year=year)

        # Filtrar por mes si se especifica
        if month:
            queryset = queryset.filter(fecha_programada__month=month)
            
        # Preparar los datos para el informe (ajusta los campos según necesites)
        informe_data = []
        for m in queryset:
            informe_data.append({
                'instalacion': m.instalacion,
                'fecha_programada': m.fecha_programada,
                'fecha_realizada': m.fecha_realizada,
                'observaciones': m.observaciones or "Sin observaciones"
            })
        context['informe_data'] = informe_data
        
        # Puedes pasar también los años y meses para el formulario
        context['years'] = [2023, 2024, 2025, 2026]  # O genera dinámicamente
        context['months'] = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
            5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
            9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        return context

        
#Crear la Vista para el Tablero Kanban
@method_decorator(csrf_exempt, name='dispatch')
class KanbanBoardView(TemplateView):
    """
    Vista basada en clases para mostrar el tablero Kanban.
    Muestra las tareas agrupadas por estado y pertenecientes a una comunidad.
    """
    template_name = "mantenimiento/kanban_board.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comunidad_id = self.kwargs.get('comunidad_id')
        comunidad = get_object_or_404(Comunidad, id=comunidad_id)
        context['comunidad'] = comunidad
        # Agrupar tareas por estado
        context['task_statuses'] = {
            'pendiente': MaintenanceTask.objects.filter(mantencion__comunidad=comunidad, status='pendiente'),
            'revision': MaintenanceTask.objects.filter(mantencion__comunidad=comunidad, status='revision'),
            'proceso': MaintenanceTask.objects.filter(mantencion__comunidad=comunidad, status='proceso'),
            'completado': MaintenanceTask.objects.filter(mantencion__comunidad=comunidad, status='completado'),
        }
        return context
    
    def post(self, request, *args, **kwargs):
        """
        Maneja las solicitudes POST para actualizar el estado de una tarea.
        """
        try:
            data = json.loads(request.body)
            task_id = data.get('task_id')
            new_status = data.get('new_status')
            
            task = MaintenanceTask.objects.get(id=task_id)
            task.status = new_status
            task.save()
            
            # Enviar notificación en tiempo real
            send_maintenance_notification(f"La tarea '{task.titulo}' se actualizó a {task.status}.")
            
            return JsonResponse({'success': True, 'new_status': task.status})
        except MaintenanceTask.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Tarea no encontrada'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
class CalendarView(TemplateView):
    template_name = "mantenimiento/Fullcalendar.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comunidad_id = self.kwargs.get('comunidad_id')
        comunidad = get_object_or_404(Comunidad, id=comunidad_id)
        context['comunidad'] = comunidad
        return context
    
class EventosMantenciones(View):
    def get(self, request, comunidad_id, *args, **kwargs):
        comunidad = get_object_or_404(Comunidad, id=comunidad_id)
        # Filtrar las tareas de mantenimiento asociadas a la comunidad
        tasks = MaintenanceTask.objects.filter(mantencion__comunidad=comunidad)
        events = []
        for task in tasks:
            # Por ejemplo, usamos la fecha_programada para eventos pendientes y fecha_realizada para los completados.
            if task.status in ['pendiente', 'programado']:
                event_date = task.fecha_programada
            else:
                event_date = task.fecha_realizada

            # Asegurarse que event_date tenga un valor válido
            if event_date:
                events.append({
                    "title": task.titulo,
                    "start": event_date.strftime("%Y-%m-%d"),
                    "description": task.descripcion,
                    "status": task.status,
                    # Agrega otros campos que necesites para personalizar el evento
                })
        return JsonResponse(events, safe=False)
    
class MantenimientoDashboardView(TemplateView):
    template_name = "mantenimiento/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Intentamos obtener una comunidad asociada al usuario
        comunidad = (self.request.user.comunidades_seguimiento.first() or
                    self.request.user.comunidades_administradas.first())
        
        if not comunidad:
            raise Http404("No se encontró comunidad para el usuario autenticado.")
        context['comunidad'] = comunidad
        
        # Filtrado general para la comunidad actual
        qs = MantencionPreventiva.objects.filter(comunidad=comunidad)
        
        # Métricas generales
        total_mantenciones = qs.count()
        total_realizadas = qs.filter(fecha_realizada__isnull=False).count()
        total_pendientes = qs.filter(fecha_realizada__isnull=True).count()
        # Instalaciones con mantenciones pendientes (sin repetir)
        instalaciones_pendientes = qs.filter(fecha_realizada__isnull=True).values_list('instalacion', flat=True).distinct().count()
        
        # Métricas por año y por mes (ejemplo para el año actual)
        año_actual = datetime.now().year
        qs_año = qs.filter(fecha_programada__year=año_actual)
        total_mantenciones_año = qs_año.count()
        total_mantenciones_mes = qs_año.filter(fecha_programada__month=datetime.now().month).count()
        
        # Calcular mantenciones por cada mes (de enero a diciembre)
        monthly_counts = [
            qs_año.filter(fecha_programada__month=month).count()
            for month in range(1, 13)
        ]
        
        context.update({
            "total_mantenciones": total_mantenciones,
            "total_realizadas": total_realizadas,
            "total_pendientes": total_pendientes,
            "instalaciones_pendientes": instalaciones_pendientes,
            "total_mantenciones_año": total_mantenciones_año,
            "total_mantenciones_mes": total_mantenciones_mes,
            # Para la lista de mantenciones recientes (últimos 5, por ejemplo)
            "mantenciones_recientes": qs.filter(fecha_realizada__isnull=False).order_by('-fecha_realizada')[:5],
            "monthly_counts": monthly_counts,  # Datos reales para el gráfico de línea
        })
        
        return context
    
def send_maintenance_notification(descripcion, fecha_inicio, fecha_fin, finalizado=False):
    """Envía una notificación a los usuarios sobre el mantenimiento."""
    channel_layer = get_channel_layer()
    notification_message = (
        f"El mantenimiento '{descripcion}' comenzará el {fecha_inicio} y finalizará el {fecha_fin}."
    )
    if finalizado:
        notification_message += " El mantenimiento ha finalizado."

    # Enviar la notificación a todos los usuarios conectados al canal de WebSocket
    async_to_sync(channel_layer.group_send)(
        "notifications",  # Nombre del grupo
        {
            "type": "send_notification",  # Llamar al método 'send_notification' del consumer
            "message": notification_message,
        }
    )






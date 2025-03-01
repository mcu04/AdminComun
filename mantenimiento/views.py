from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, TemplateView
from django.urls import reverse_lazy
from .models import (MantencionPreventiva, ContratoMantenimiento, ReparacionGeneral, CotizacionProveedor, Proveedor)
from .forms import (
    MantencionPreventivaForm, 
    ContratoMantenimientoForm, 
    ReparacionGeneralForm, 
    CotizacionProveedorForm, 
    ProveedorForm
)
from .filters import MantencionPreventivaFilter
from django.views.generic import ListView
import django_filters
from django_filters.views import FilterView
from django.http import JsonResponse
from Aplicaciones.seguimientodocumentos.models import Comunidad



# Mantención Preventiva
class MantencionPreventivaListView(FilterView):
    model = MantencionPreventiva
    template_name = "mantenimiento/mantencion_list.html"
    filterset_class = MantencionPreventivaFilter  # Aquí usas tu clase de filtros
    context_object_name = "mantenciones"
    
    def get_queryset(self):
        # Filtra por la comunidad indicada en la URL
        qs = super().get_queryset()
        comunidad_id = self.kwargs.get('comunidad_id')
        return qs.filter(comunidad_id=comunidad_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comunidad_id = self.kwargs.get('comunidad_id')  # Obtiene comunidad_id desde la URL
        
        context['comunidad'] = get_object_or_404(Comunidad, id=comunidad_id)  # Asegura que exista
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
    success_url = reverse_lazy('mantenimiento:dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comunidad_id = self.kwargs.get('comunidad_id')
        context['comunidad'] = get_object_or_404(Comunidad, id=comunidad_id)  # Asegurar comunidad
        return context

    def get_success_url(self):
        return reverse_lazy('mantenimiento:mantencion_list', kwargs={'comunidad_id': self.kwargs.get('comunidad_id')})

# Contratos Empresas de Mantenimiento
class ContratoMantenimientoListView(ListView):
    model = ContratoMantenimiento
    template_name = "mantenimiento/contrato_list.html"
    context_object_name = "contratos"

class ContratoMantenimientoCreateView(CreateView):
    model = ContratoMantenimiento
    form_class = ContratoMantenimientoForm
    template_name = "mantenimiento/contrato_form.html"
    success_url = reverse_lazy('mantenimiento:dashboard')

# Reparaciones Generales
class ReparacionGeneralListView(ListView):
    model = ReparacionGeneral
    template_name = "mantenimiento/reparacion_list.html"
    context_object_name = "reparaciones"

class ReparacionGeneralCreateView(CreateView):
    model = ReparacionGeneral
    form_class = ReparacionGeneralForm
    template_name = "mantenimiento/reparacion_form.html"
    success_url = reverse_lazy('mantenimiento:dashboard')

# Cotizaciones de Proveedores
class CotizacionProveedorListView(ListView):
    model = CotizacionProveedor
    template_name = "mantenimiento/cotizacion_list.html"
    context_object_name = "cotizaciones"

class CotizacionProveedorCreateView(CreateView):
    model = CotizacionProveedor
    form_class = CotizacionProveedorForm
    template_name = "mantenimiento/cotizacion_form.html"
    success_url = reverse_lazy('mantenimiento:dashboard')

# Proveedores en el Mercado
class ProveedorListView(ListView):
    model = Proveedor
    template_name = "mantenimiento/proveedor_list.html"
    context_object_name = "proveedores"

class ProveedorCreateView(CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = "mantenimiento/proveedor_form.html"
    success_url = reverse_lazy('mantenimiento:dashboard')
    
def actualizar_dashboard(request):
    data = {
        'total_mantenciones': MantencionPreventiva.objects.count(),
        'total_pendientes': ReparacionGeneral.objects.filter(estado="Pendiente").count(),
    }
    return JsonResponse(data)

# Dashboard que resume la información de mantenimiento
class MantenimientoDashboardView(TemplateView):
    template_name = "mantenimiento/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comunidad'] = Comunidad.objects.filter(usuarios=self.request.user).first()  # Obtiene la primera comunidad del usuario
        context['mantenciones'] = MantencionPreventiva.objects.all()
        context['contratos'] = ContratoMantenimiento.objects.all()
        context['reparaciones'] = ReparacionGeneral.objects.all()
        context['cotizaciones'] = CotizacionProveedor.objects.all()
        context['proveedores'] = Proveedor.objects.all()
        # Información en “tiempo real” (conteos y últimos registros)
        context['total_mantenciones'] = MantencionPreventiva.objects.count()
        context['total_reparaciones_pendientes'] = ReparacionGeneral.objects.filter(estado="Pendiente").count()
        context['total_contratos'] = ContratoMantenimiento.objects.count()
        context['total_reparaciones'] = ReparacionGeneral.objects.count()
        return context





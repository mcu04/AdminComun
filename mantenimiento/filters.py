import django_filters
from .models import MantencionPreventiva

class MantencionPreventivaFilter(django_filters.FilterSet):
    # Filtra por fecha a partir de una fecha dada (>=)
    fecha = django_filters.DateFilter(lookup_expr='gte', label="Fecha desde")
    
    class Meta:
        model = MantencionPreventiva
        fields = ['instalacion', 'fecha']
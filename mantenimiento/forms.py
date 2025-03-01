from django import forms
from .models import MantencionPreventiva, ContratoMantenimiento, ReparacionGeneral, CotizacionProveedor, Proveedor

class MantencionPreventivaForm(forms.ModelForm):
    class Meta:
        model = MantencionPreventiva
        fields = ['instalacion', 'fecha', 'descripcion']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ContratoMantenimientoForm(forms.ModelForm):
    class Meta:
        model = ContratoMantenimiento
        fields = ['instalacion', 'empresa', 'contrato', 'contacto', 'telefono', 'valor_servicio', 'periodo', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class ReparacionGeneralForm(forms.ModelForm):
    class Meta:
        model = ReparacionGeneral
        fields = ['area', 'problema', 'estado']
        widgets = {
            'problema': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CotizacionProveedorForm(forms.ModelForm):
    class Meta:
        model = CotizacionProveedor
        fields = ['proveedor', 'servicio', 'monto', 'fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'servicios']
        widgets = {
            'servicios': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

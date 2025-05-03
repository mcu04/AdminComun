from django import forms
from .models import MantencionPreventiva
from .models import MantencionPreventiva, InstallationCategory
from django.forms.widgets import DateInput
from .models import InstalacionPreventiva
from .models import MantencionPreventiva, STATUS_CHOICES, PERIODO_CHOICES


class MantencionPreventivaForm(forms.ModelForm):
    class Meta:
        model = MantencionPreventiva
        fields = [
            'category',
            'custom_category',
            'fecha_programada', 
            'fecha_realizada', 
            'descripcion',
            'observaciones',
            'status',
            'periodo',
            'responsable',
            'costo',
        ]
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-control',
                'title': 'Seleccione una instalación'
            }),
            'custom_category': forms.TextInput(attrs={
                'class': 'form-control',
                'title': 'Ingrese otra instalación si no aparece en la lista'
            }),
            'fecha_programada': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'
            ),
            'fecha_realizada': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control'},
                format='%Y-%m-%d'
            ),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'periodo': forms.Select(attrs={'class': 'form-control'}),
            'responsable': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del responsable de la mantencion'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control'}),
            
        }
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configuramos los formatos de fecha para que el widget muestre el valor en formato ISO
        self.fields['fecha_programada'].widget.format = '%Y-%m-%d'
        self.fields['fecha_realizada'].widget.format = '%Y-%m-%d'
        self.fields['fecha_programada'].input_formats = ['%Y-%m-%d']
        self.fields['fecha_realizada'].input_formats = ['%Y-%m-%d']
        # Aseguramos que el queryset del campo 'category' contenga todos los registros
        self.fields['category'].queryset = InstallationCategory.objects.all()
    
    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        custom = cleaned_data.get('custom_category')
        # Si no se selecciona una categoría predefinida, el campo custom es obligatorio.
        if not category and not custom:
            raise forms.ValidationError("Debe seleccionar una instalación predefinida o ingresar una instalación personalizada.")
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Asigna al campo "instalacion" el nombre de la categoría si se seleccionó, o el valor del campo personalizado.
        if self.cleaned_data.get('category'):
            instance.instalacion = self.cleaned_data.get('category').name
        else:
            instance.instalacion = self.cleaned_data.get('custom_category')
        
        # Se asegura que la comunidad se asigne (en caso de edición, puede venir desde initial)
        comunidad_id = self.initial.get('comunidad_id')
        if comunidad_id:
            instance.comunidad_id = comunidad_id
            
    
        if commit:
            instance.save()
            # El modelo se encarga de sincronizar InstalacionPreventiva en su método save()
        return instance
            







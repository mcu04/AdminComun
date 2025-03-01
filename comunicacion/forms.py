from django import forms
from Aplicaciones.seguimientodocumentos.models import Comunidad
from .models import CorreoAdjunto, Archivo, Destinatario
from .widgets import MultiFileInput  # Widget personalizado (ver sección Widgets, si es necesario)
from django.db.models import Q
from .fields import MultiFileField

class MultiFileField(forms.FileField):
    widget = MultiFileInput

    def to_python(self, data):
        # Si no hay datos, retorna una lista vacía en lugar de None
        if not data:
            return []
        return data

class EnviarCorreoIndividualForm(forms.Form):
    """
    Formulario para enviar un correo individual.
    Permite seleccionar un destinatario, ingresar asunto, mensaje y adjuntar múltiples archivos.
    """
    destinatario = forms.ModelChoiceField(
        queryset=Destinatario.objects.none(),  # Se actualizará en __init__
        label="Destinatario",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    asunto = forms.CharField(
        label="Asunto",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    mensaje = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
    archivos_adjuntos = MultiFileField(
        label="Adjuntar archivos",
        required=False
    )

    def __init__(self, *args, **kwargs):
        
        # Extraer 'request' si se pasa, sino, tratar de extraer 'user'
        request = kwargs.pop('request', None)  # Esperamos recibir el objeto request
        super(EnviarCorreoIndividualForm, self).__init__(*args, **kwargs)
        
        if request:
            comunidad_id = request.session.get('comunidad_id')
            if comunidad_id:
                self.fields['destinatario'].queryset = Destinatario.objects.filter(comunidad_id=comunidad_id)
            else:
                self.fields['destinatario'].queryset = Destinatario.objects.none()
        else:
            self.fields['destinatario'].queryset = Destinatario.objects.all()
            

class EnviarCorreoMasivoForm(forms.Form):
    """
    Formulario para enviar un correo masivo.
    
    """
    destinatarios = forms.ModelMultipleChoiceField(
        queryset=Destinatario.objects.none(),  # Se actualizará en __init__
        label="Destinatarios",
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    asunto = forms.CharField(
        label="Asunto",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    mensaje = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
    
    archivos_adjuntos = MultiFileField(
        label="Adjuntar archivos",
        required=False
    )
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(EnviarCorreoMasivoForm, self).__init__(*args, **kwargs)

        if request:
            comunidad_id = request.session.get('comunidad_id')
            if comunidad_id:
                qs = Destinatario.objects.filter(comunidad_id=comunidad_id)
                self.fields['destinatarios'].queryset = qs
                # Preseleccionar todos los destinatarios
                self.initial['destinatarios'] = qs
            else:
                self.fields['destinatarios'].queryset = Destinatario.objects.none()
        else:
            qs = Destinatario.objects.all()
            self.fields['destinatarios'].queryset = qs
            self.initial['destinatarios'] = qs
    
    
        
class CorreoAdjuntoForm(forms.ModelForm):
    class Meta:
        model = CorreoAdjunto
        fields = ['archivo']
        widgets = {
            'archivo': MultiFileInput(attrs={'class': 'form-control'})
        }
        
class ArchivoForm(forms.ModelForm):
    class Meta:
        model = Archivo
        fields = ['archivo']
        widgets = {
            'archivo': MultiFileInput(attrs={'class': 'form-control'})
        }

class DestinatarioForm(forms.ModelForm):
    class Meta:
        model = Destinatario
        fields = ['nombre', 'apellido', 'correo']  # No incluimos comunidad, se asigna automáticamente
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
        }
    # Opcionalmente, personaliza los widgets:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
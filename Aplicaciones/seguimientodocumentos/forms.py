from django import forms
from Aplicaciones.seguimientodocumentos.models import Seguimiento, Documentacion
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.apps import apps
from Aplicaciones.seguimientodocumentos.models import Comunidad
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator


class SeguimientoForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('seguimientodocumentos', 'Seguimiento')  # Import diferido
        fields = ['documentacion', 'existe', 'observaciones']
        widgets = {
            'documentacion': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccionar documentación'
                }),
            'existe': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': '¿El documento existe?'
                }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Escribir las observaciones',
                'rows': 5,  # Define el número de filas del textarea
            }),
        }
    def __init__(self, *args, **kwargs):
        super(SeguimientoForm, self).__init__(*args, **kwargs)
        # Si necesitas lógica adicional, puedes agregarla aquí
        for field_name, field in self.fields.items():
            field.widget.attrs['autocomplete'] = 'off'  # Desactiva el autocompletado
            if field_name == 'documentacion':
                field.label = 'Documento relacionado'  # Personaliza la etiqueta del campo
                
    def clean(self):
        cleaned_data = super().clean()
        existe = cleaned_data.get('existe')
        observaciones = cleaned_data.get('observaciones')

            # Valida que se agregue una observación si el documento no existe
        if existe == 'No' and not observaciones:
            raise forms.ValidationError(
                "Debes agregar una observación si el documento no existe."
            )
        return cleaned_data
    


class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'tuemail@ejemplo.com'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Crea tu usuario'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Crea una contraseña segura'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Confirma tu contraseña'
            }),
        }

              
class DocumentacionForm(forms.ModelForm):
    class Meta:
            model = Documentacion
            fields = ['tipo', 'categoria', 'titulo_documento', 'comunidad']
            widgets = {
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'comunidad': forms.Select(attrs={'class': 'form-control'}),
            
    }    
    def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)  # Capturamos el usuario autenticado
            super().__init__(*args, **kwargs)
            if user:
            # Filtrar las comunidades que pertenece al usuario autenticado
                self.fields['comunidad'].queryset = Comunidad.objects.filter(administrador=user)

    def save(self, commit=True):
            instance = super().save(commit=False)
            # Asociar comunidad del usuario actual
            instance.comunidad = self.user.comunidades.first()
            if commit:
                instance.save()
            return instance
        
class ComunidadForm(forms.ModelForm):
    class Meta:
        model = Comunidad
        fields = ['nombre', 'direccion', 'descripcion', ]  # Ajusta los campos necesarios 'administrador'
        

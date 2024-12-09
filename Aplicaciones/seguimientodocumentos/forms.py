from django import forms
from .models import seguimiento
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SeguimientoForm(forms.ModelForm):
    class Meta:
        model = seguimiento
        fields = ['documentacion', 'existe', 'observaciones']
        widgets = {
            'documentacion': forms.Select(attrs={'class': 'form-control'}),
            'existe': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Escribir las observaciones',
                'rows': 5,  # Define el número de filas del textarea
            }),
            'fecha_actualizado': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',  # Usa un selector de fecha moderno si el navegador lo soporta
            }),            
                
        }
        
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'tuemail@ejemplo.com'
    }))

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
        




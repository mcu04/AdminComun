from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm

# Formulario personalizado para el registro de usuarios
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
# Solicitar el restablecimiento (ingresar el correo)
class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Correo Electrónico", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
# Cambiar la contraseña
class PasswordResetConfirmForm(forms.Form):
    new_password = forms.CharField(label="Nueva Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}), validators=[validate_password])
    confirm_password = forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("new_password")
        p2 = cleaned_data.get("confirm_password")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data
    
class AuthenticationWithTermsForm(AuthenticationForm):
    accept_terms = forms.BooleanField(
        label="He leído y acepto los <a href='{url}' target='_blank'>Términos y Condiciones</a>".format(
            url="{% static 'docs/terminos_condiciones.pdf' %}"
        ),
        error_messages={'required': 'Debes aceptar los Términos y Condiciones para entrar.'},
        widget=forms.CheckboxInput(),
        required=True,
    )
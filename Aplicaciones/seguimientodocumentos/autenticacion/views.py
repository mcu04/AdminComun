from django.shortcuts import render, redirect, get_object_or_404, reverse
from .forms import RegistroForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .forms import PasswordResetRequestForm, PasswordResetConfirmForm
from .models import PasswordResetToken
from django.contrib.auth import authenticate, login
from django.utils.http import url_has_allowed_host_and_scheme 
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from urllib.parse import urlencode
from django.contrib.auth.forms import AuthenticationForm
from Aplicaciones.seguimientodocumentos.autenticacion.models import Profile
from django.middleware.csrf import get_token
from .forms import AuthenticationWithTermsForm
from django.views.decorators.csrf import csrf_protect




def registrarse(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente después del registro
            messages.success(request, "¡Registro exitoso! Bienvenido a la plataforma.")
            return redirect('seguimientodocumentos:home')
        else:
            messages.error(request, "Por favor, corrige los errores a continuación.")
    else:
        form = RegistroForm()
    return render(request, 'seguimientodocumentos/registrarse.html', {'form': form})

# Recibe el correo, busca el usuario, genera un token y envía un email.
User = get_user_model()

def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                user = User.objects.get(email=email)
                # Genera un token
                token_obj = PasswordResetToken.objects.create(user=user)
                # Construir el enlace; aquí evitamos depender de django.contrib.sites:
                reset_link = request.build_absolute_uri(
                    reverse("autenticacion:password_reset_confirm", kwargs={"token": token_obj.token})
                )
                # Envía el correo
                subject = "Restablecimiento de contraseña para Manon Group"
                message = f"Hola {user.username},\n\nHas solicitado restablecer tu contraseña.\nPor favor, haz clic en el siguiente enlace para establecer una nueva contraseña:\n\n{reset_link}\n\nSi no solicitaste este cambio, ignora este correo.\n\n¡Gracias!"
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
                messages.success(request, "Si existe una cuenta con ese correo, recibirás instrucciones para restablecer tu contraseña.")
                return redirect("autenticacion:password_reset_request")
            except User.DoesNotExist:
                messages.success(request, "Si existe una cuenta con ese correo, recibirás instrucciones para restablecer tu contraseña.")
                return redirect("autenticacion:password_reset_request")
    else:
        form = PasswordResetRequestForm()
    return render(request, "autenticacion/password_reset_request.html", {"form": form})

# Recibe el token, valida su vigencia y permite al usuario ingresar la nueva contraseña.
def password_reset_confirm(request, token):
    token_obj = get_object_or_404(PasswordResetToken, token=token)
    if not token_obj.is_valid():
        messages.error(request, "El enlace de restablecimiento ha expirado.")
        return redirect("autenticacion:password_reset_request")
    if request.method == "POST":
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data["new_password"]
            user = token_obj.user
            user.set_password(new_password)
            user.save()
            # Opcional: eliminar el token después de usarlo
            token_obj.delete()
            messages.success(request, "Tu contraseña ha sido restablecida exitosamente.")
            return redirect("seguimientodocumentos:iniciar_sesion")
    else:
        form = PasswordResetConfirmForm()
    return render(request, "autenticacion/password_reset_confirm.html", {"form": form})

@csrf_protect
def iniciar_sesion(request):
    next_url = request.GET.get('next') or reverse('seguimientodocumentos:comunidades')

    if request.method == "POST":
        form = AuthenticationWithTermsForm(data=request.POST)
        if form.is_valid():
            # Aquí sabemos que accept_terms=True porque es required
            user = form.get_user()
            login(request, user)
            # Marcamos en el perfil que aceptó T&C
            profile = getattr(user, 'profile', None)
            if profile:
                profile.accepted_terms = True
                profile.save()
            return redirect('/')  
    else:
        form = AuthenticationWithTermsForm()
        get_token(request)

    return render(request, 'autenticacion/iniciar_sesion.html', {
        'form': form,
        'next': next_url,
    })


@login_required
def terminos_condiciones(request):
    # Primero de POST, si no de GET
    next_url = request.POST.get('next') or request.GET.get('next') or reverse('seguimientodocumentos:comunidades')

    if request.method == "POST":
        # Perfil siempre existe gracias a la señal
        profile = request.user.profile
        profile.accepted_terms = True
        profile.save()
        return redirect(next_url)

    return render(request, 'autenticacion/terminos_condiciones.html', {
        'next': next_url,
    })


@login_required
def cerrar_sesion(request):
    # Limpiar la sesión completamente, eliminando todos los datos y mensajes previos
    request.session.flush()
    
    # Cierra la sesión del usuario
    logout(request)
    
    # Obtiene el parámetro 'next' si está presente, o usa '/' por defecto
    next_url = request.GET.get('next', '/')
    
    # Prepara la redirección a la página de inicio de sesión
    query_string = urlencode({'next': next_url.strip()})
    
    # Redirige a la página de inicio de sesión con el parámetro 'next'
    return redirect(f"{reverse('autenticacion:iniciar_sesion')}?{query_string}")







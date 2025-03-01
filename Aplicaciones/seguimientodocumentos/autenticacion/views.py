from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import RegistroForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .forms import PasswordResetRequestForm, PasswordResetConfirmForm
from .models import PasswordResetToken

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









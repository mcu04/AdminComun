from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroForm
from django.contrib import messages

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








"""

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db import IntegrityError

def registrarse(request):
    if request.method == "GET":
        return render(request, "registrarse.html", {"form": UserCreationForm()})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect("seguimientodocumentos:listar_seguimiento")
            except IntegrityError:
                messages.error(request, "El usuario ya existe.")
                return render(request, "registrarse.html", {"form": UserCreationForm()})
        else:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, "registrarse.html", {"form": UserCreationForm()})
"""
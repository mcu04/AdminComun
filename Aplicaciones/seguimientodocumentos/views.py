# from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from .models import seguimiento, documentacion
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import SeguimientoForm   # Crearás este formulario
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import RegistroForm
from django.contrib import messages
from urllib.parse import urlencode
from django.urls import reverse




    # Create your views here.


def home(request):
    return render(request, "home.html")


def registrarse(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente después del registro
            messages.success(request, "¡Registro exitoso! Bienvenido a la plataforma.")
            return redirect('seguimientodocumentos:pagina_inicio')
        else:
            messages.error(request, "Por favor, corrige los errores a continuación.")
    else:
        form = RegistroForm()
    return render(request, 'seguimientodocumentos/registrarse.html', {'form': form})

@login_required
def detallesseguimiento(request, seguimiento_id):
    if request.method == 'GET':
        seguimiento_instance =get_object_or_404(seguimiento, pk=seguimiento_id)
        form = SeguimientoForm(instance=seguimiento_instance)
        return render(request, 'detalle_seguimiento.html', {
            'seguimiento_instance':seguimiento_instance, 'form': form})
    else:
        try:
            seguimiento_instance=get_object_or_404(seguimiento, pk=seguimiento_id)
            form= SeguimientoForm(request.POST, instance=seguimiento_instance)
            if form.is_valid():
                form.save()
                return redirect('seguimientodocumentos:seguimiento')
        except ValueError:
            return render(request, 'detalle_seguimiento.html', {
            'seguimiento_instance': seguimiento_instance,
            'form': form,
            'error': 'Error al actualizar los datos'
        })

@login_required
def actualizar_seguimiento(request, seguimiento_id):
    # Obtener el objeto desde la base de datos con un nombre distinto para evitar conflictos
    objeto_seguimiento = get_object_or_404(seguimiento, pk=seguimiento_id)
        
    if request.method == 'POST':
        # Procesar los datos enviados en el formulario
        form = SeguimientoForm(request.POST, instance=objeto_seguimiento)
        if form.is_valid():
            # Guardar el seguimiento actualizado
            seguimiento_actualizado = form.save(commit=False)
            seguimiento_actualizado.fecha_actualizado = timezone.now()  # Opcional, si quieres actualizar automáticamente
            seguimiento_actualizado.save()
            return redirect('seguimientodocumentos:detalle_seguimiento', seguimiento_id=seguimiento_actualizado.id)

    else:
        # Mostrar el formulario con los datos actuales
        form = SeguimientoForm(instance=objeto_seguimiento)
        
        # Renderizar la plantilla con el formulario
        return render(
        request,
        'detalle_seguimiento.html',
        {'form': form, 'seguimiento': objeto_seguimiento, 'seguimiento_id': seguimiento_id}
    )
    
@login_required           
def seguimiento_pendiente(request):
    seguimientos = seguimiento.objects.filter(fecha_actualizado__isnull=True)  # Filtra no actualizados
    return render(request, 'seguimiento_pendiente.html', {'seguimientos': seguimientos})
  

@login_required    
def eliminar_seguimiento(request, id):
        seguimiento_instance = get_object_or_404(seguimiento, pk=id)
        if request.method == 'POST':
            seguimiento_instance.delete()
            return redirect('seguimientodocumentos:seguimiento_pendiente')
        return render(request, 'confirmar_eliminar.html', {'seguimiento': seguimiento})

@login_required
def crear_seguimiento(request):
    if request.method == 'GET':
        form = SeguimientoForm()
        return render(request, 'crear_seguimiento.html', {
            'form': form,
            
        })
    else:
        form = SeguimientoForm(request.POST)
        if form.is_valid():  # Valida los datos del formulario
            try:
                nuevo_seguimiento = form.save (commit=False) # Guarda sin confirmar para añadir lógica extra
                #nuevo_seguimiento.user = request.user
                nuevo_seguimiento.save()       # Ahora guarda el seguimiento en la base de datos
                return redirect("seguimientodocumentos:seguimiento_pendiente")  # Asegúrate de que este nombre de URL sea correcto
            except Exception as e:
                # Registro del error en los logs
                import logging
                logging.error(f"Error al guardar el seguimiento: {e}")
                # Retornar el formulario con el error
                return render(request, 'crear_seguimiento.html', {
                    'form': form,
                    'error': f'Error al guardar el seguimiento: {str(e)}',
                                        
                })
            else:
                # Si el formulario no es válido, vuelve a renderizar con errores
                return render(request, 'crear_seguimiento.html', {
                'form': form,
                'error': 'Formulario no válido. Por favor, verifica los datos.',
                
            })

@login_required
def listar_seguimiento(request):
    # Consulta registros de seguimientos filtrados
    seguimientos = seguimiento.objects.filter(existe='Si').order_by('-fecha_actualizado')
    return render(request, 'seguimiento.html', {'seguimiento': seguimientos})

@login_required      
def cerrar_sesion(request):
    from django.contrib.auth import logout
    logout(request)
    next_url = request.GET.get('next', '/')
    query_string = urlencode({'next': next_url.strip()})
    return redirect(f"{reverse('seguimientodocumentos:iniciar_sesion')}?{query_string}")

def iniciar_sesion(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["Usuario"],
            password=request.POST["password"],
        )
        if user is None:
            return render(request, "iniciar_sesion.html", {
                "error": 'Usuario o Contraseña es incorrecta'
            })
        else:
            login(request, user)
            remember_me = request.POST.get("remember")
            if not remember_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(1209600)  # 2 semanas
            return redirect(request.POST.get("next", "home"))
    else:
        return render(request, "iniciar_sesion.html")

def pagina_inicio(request):
        return render(request, 'inicio.html')  # Cambia a tu plantilla deseada
    
def pagina_principal(request):
    return render(request, 'pagina_principal.html')
        


        







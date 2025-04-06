from django.shortcuts import render, redirect,  get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Aplicaciones.seguimientodocumentos.models import Comunidad
from .forms import EnviarCorreoIndividualForm, EnviarCorreoMasivoForm, CorreoAdjuntoForm, ArchivoForm, DestinatarioForm
from .models import Archivo, Destinatario, CorreoAdjunto
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
import json


def index(request):
    return render (request, 'comunicacion/index.html')  # Asegura que el template esté en la ruta correcta

def contacto(request):

    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        
        template = render_to_string('comunicacion/email-template.html', {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
        
        })
        
        emailSender = EmailMessage(
            subject,
            template,
            settings.EMAIL_HOST_USER,
            ['marionelson@manon.cl', 'mariocarrenourbina@gmail.com' ]
        )
        
        emailSender.content_subtype= 'html'
        emailSender.fail_silently= False
        emailSender.send()
        
        messages.success(request, 'El correo electronico se envio correctamente')
                
    return redirect ('comunicacion:index')

@login_required
def enviar_correo_individual(request, comunidad_id):
    # Obtén el objeto comunidad
    comunidad = get_object_or_404(Comunidad, pk=comunidad_id)
    
    if request.method == "POST":
        form = EnviarCorreoIndividualForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            destinatario = form.cleaned_data["destinatario"]
            asunto = form.cleaned_data["asunto"]
            mensaje = form.cleaned_data["mensaje"]
            archivos = request.FILES.getlist("archivos_adjuntos")
            
            email = EmailMessage(
                subject=asunto,
                body=mensaje,
                from_email=settings.EMAIL_HOST_USER,
                to=[destinatario.correo],
            )
            
            for archivo in archivos:
                email.attach(archivo.name, archivo.read(), archivo.content_type)
            
            try:
                email.send()
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({"success": True, "message": "Correo enviado correctamente."})
                
                messages.success(request, "Correo individual enviado correctamente.")
                return redirect("comunicacion:enviar_correo_individual", comunidad_id=comunidad_id)
            
            except Exception as e:
                error_msg = f"Error al enviar el correo: {str(e)}"
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({"success": False, "message": error_msg}, status=500)
                messages.error(request, error_msg)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "errors": form.errors}, status=400)
            messages.error(request, "Error en el formulario. Verifique los campos.")
        
        return render(request, "comunicacion/enviar_correo_individual.html", {"form": form, "comunidad": comunidad, "comunidad_id": comunidad.id})
    else:
        form = EnviarCorreoIndividualForm(request=request)
    return render(request, "comunicacion/enviar_correo_individual.html", {"form": form, "comunidad": comunidad,"comunidad_id": comunidad.id})

@login_required
def enviar_correo_masivo(request, comunidad_id):
    comunidad = get_object_or_404(Comunidad, pk=comunidad_id)
    
    if request.method == "POST":
        form = EnviarCorreoMasivoForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            asunto = form.cleaned_data["asunto"]
            mensaje = form.cleaned_data["mensaje"]
            destinatarios_qs = form.cleaned_data["destinatarios"]
            archivos = request.FILES.getlist("archivos_adjuntos")
            
            lista_correos = [dest.correo for dest in destinatarios_qs]
            
            email = EmailMessage(
                subject=asunto,
                body=mensaje,
                from_email=settings.EMAIL_HOST_USER,
                to=lista_correos,
            )
            for archivo in archivos:
                email.attach(archivo.name, archivo.read(), archivo.content_type)
                
            try:
                email.send()
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({"success": True, "message": "Correo masivo enviado correctamente."})
                messages.success(request, "Correo masivo enviado correctamente.")
                return redirect("comunicacion:enviar_correo_masivo", comunidad_id=comunidad_id)
            except Exception as e:
                error_msg = f"Error al enviar el correo: {str(e)}"
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({"success": False, "message": error_msg}, status=500)
                messages.error(request, error_msg)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "errors": form.errors}, status=400)
            messages.error(request, "Error en el formulario. Verifique los campos.")
        return render(request, "comunicacion/enviar_correo_masivo.html", {"form": form, "comunidad": comunidad, "comunidad_id": comunidad.id})
    else:
        form = EnviarCorreoMasivoForm(request=request)
    return render(request, "comunicacion/enviar_correo_masivo.html", {"form": form, "comunidad": comunidad, "comunidad_id": comunidad.id})

def gestionar_destinatarios(request):
    """
    Vista para agregar y listar destinatarios, filtrando solo los que pertenecen a la comunidad actual
    (almacenada en la sesión).
    """
    # Obtener la comunidad actual desde la sesión
    comunidad_id = request.session.get('comunidad_id')
    
    if not comunidad_id:
        messages.error(request, "No tienes una comunidad asignada. Por favor selecciona una comunidad.")
        return redirect("seguimientodocumentos:comunidades")  # Ajusta la URL según tu configuración

    # Recuperar la comunidad para asignarla en el formulario
    comunidad = get_object_or_404(Comunidad, id=comunidad_id)
    
    if request.method == "POST":
        form = DestinatarioForm(request.POST)
        if form.is_valid():
            # Crear el objeto sin guardarlo aún
            destinatario = form.save(commit=False)
            destinatario.user = request.user
            destinatario.comunidad = comunidad  # Asigna la comunidad actual
            destinatario.save()
            messages.success(request, "Destinatario agregado correctamente.")
            return redirect("comunicacion:gestionar_destinatarios")
        else:
            messages.error(request, "Error al agregar destinatario. Verifica los campos.")
    else:
        form = DestinatarioForm()
    
    # Filtrar la lista de destinatarios según la comunidad actual
    destinatarios = Destinatario.objects.filter(comunidad=comunidad)
    context = {
        "form": form,
        "destinatarios": destinatarios,
        "comunidad": comunidad,
    }
    return render(request, "comunicacion/gestionar_destinatarios.html", context)

@login_required
def enviar_correo(request):
    """Vista para enviar correos con archivos adjuntos.
    Permite seleccionar una comunidad, ingresar asunto y mensaje, y adjuntar múltiples archivos."""
    
    if request.method == "POST":
        form = EnviarCorreoIndividualForm(request.POST, request.FILES, user=request.user)
        
        if form.is_valid():
            comunidad = form.cleaned_data["comunidad"]
            asunto = form.cleaned_data["asunto"]
            mensaje = form.cleaned_data["mensaje"]
            # Gracias al widget personalizado, esto será una lista de archivos:
            archivos = request.FILES.getlist("archivos_adjuntos")
            
            # Configurar destinatarios (ajusta la lógica según tus necesidades)
            destinatarios = ["destinatario@gmail.com"]  # Ejemplo: reemplazar con los destinatarios reales
            
            # Configurar el correo
            email = EmailMessage(
                subject=asunto,
                body=f"Comunidad: {comunidad}\n\n{mensaje}",
                from_email="contacto@manon.cl",  # Cambiar por tu correo real
                to=destinatarios,
            )
            
            # Adjuntar archivos si existen
            if archivos:
                for archivo in archivos:
                    email.attach(archivo.name, archivo.read(), archivo.content_type)
            
            try:
                email.send()
                messages.success(request, "Correo enviado correctamente.")
                return redirect("enviar_correo")
            except Exception as e:
                messages.error(request, f"Error al enviar el correo: {str(e)}")

        else:
            messages.error(request, "Error en el formulario. Verifique los campos.")

    else:
        form = EnviarCorreoIndividualForm(user=request.user)

    return render(request, "comunicacion/enviar_correo.html", {"form": form})

def subir_archivos(request):
    """Vista para subir múltiples archivos."""
    
    if request.method == "POST":
        form = ArchivoForm(request.POST, request.FILES)
        archivos = request.FILES.getlist('archivo')  # Obtener múltiples archivos
        
        if archivos:
            for archivo in archivos:
                Archivo.objects.create(archivo=archivo)
            messages.success(request, "Archivo(s) subido(s) correctamente.")
            return redirect('subir_archivos')
        else:
            messages.error(request, "Debes seleccionar al menos un archivo.")

    else:
        form = ArchivoForm()
    
    return render(request, 'comunicacion/subir_archivos.html', {'form': form})

class DestinatarioListView(LoginRequiredMixin, ListView):
    model = Destinatario
    template_name = "comunicacion/destinatario_list.html"
    context_object_name = "destinatarios"

    def get_queryset(self):
        # Filtrar destinatarios del usuario actual
        return Destinatario.objects.filter(user=self.request.user)
    
class DestinatarioCreateView(LoginRequiredMixin, CreateView):
    model = Destinatario
    form_class = DestinatarioForm
    template_name = "comunicacion/destinatario_form.html"
    success_url = reverse_lazy("comunicacion:gestionar_destinatarios")

    def form_valid(self, form):
        # Asigna el usuario y la comunidad por defecto
        form.instance.user = self.request.user
        
        # Buscar comunidades donde el usuario es miembro o administrador.
        comunidades_miembro = Comunidad.objects.filter(usuarios=self.request.user)
        # Obtener comunidades donde el usuario es administrador
        comunidades_admin = Comunidad.objects.filter(administrador=self.request.user)
        # Combinar ambas queryset
        comunidades = (comunidades_miembro | comunidades_admin).distinct()
        
        if comunidades.exists():
            # Asignar la primera comunidad (puedes ajustar esta lógica si hay más de una)
            form.instance.comunidad = comunidades.first()
        else:
            form.add_error(None, "No tienes una comunidad asignada.")
            return self.form_invalid(form)
        return super().form_valid(form)
    
class DestinatarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Destinatario
    form_class = DestinatarioForm
    template_name = "comunicacion/destinatario_form.html"
    success_url = reverse_lazy("comunicacion:gestionar_destinatarios")
    
class DestinatarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Destinatario
    template_name = "comunicacion/destinatario_confirm_delete.html"
    success_url = reverse_lazy("comunicacion:gestionar_destinatarios")
    
def obtener_destinatarios(request):
    """
    Devuelve una lista de destinatarios en formato JSON.
    """
    comunidad_id = request.session.get('comunidad_id')
    destinatarios = Destinatario.objects.filter(comunidad_id=comunidad_id).values("id", "nombre", "correo")

    return JsonResponse({"destinatarios": {d["id"]: f"{d['nombre']} ({d['correo']})" for d in destinatarios}})


# Verifica que el usuario en cuestión (por ejemplo, "Manon3") sea el administrador de algunas comunidades
from django.contrib.auth.models import User
from Aplicaciones.seguimientodocumentos.models import Comunidad
user = User.objects.get(username='Manon3')
comunidades_admin = Comunidad.objects.filter(administrador=user)
#print(comunidades_admin)

from django.contrib.auth.models import User
from Aplicaciones.seguimientodocumentos.models import Comunidad
from comunicacion.models import Destinatario

user = User.objects.get(username='Manon3')
# Verifica comunidades (tanto por ser miembro como administrador)
comunidades = Comunidad.objects.filter(usuarios=user) | Comunidad.objects.filter(administrador=user)
#print(comunidades.distinct())
# Verifica destinatarios asociados a esas comunidades:
destinatarios = Destinatario.objects.filter(comunidad__in=comunidades.distinct())
#print(destinatarios)
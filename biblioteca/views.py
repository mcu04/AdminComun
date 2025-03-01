from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse, HttpResponseForbidden
from biblioteca.models import Documento
import requests
from .models import Documento, Archivo # Asegúrate de tener un modelo Archivo definido
from Aplicaciones.seguimientodocumentos.models import Comunidad
from .forms import ArchivoForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db import models


# Create your views here.

@login_required
def biblioteca_lista(request):
    comunidad_id = request.sesion['comunidad_id']
    documentos = Documento.objects.all()
    return render(request, 'biblioteca/lista.html', {'documentos': documentos, 'comunidad_id': comunidad_id})
@login_required
def biblioteca_detalle(request, pk):
    documento = get_object_or_404(Documento, pk=pk)
    return render(request, 'biblioteca/detalle.html', {'documento': documento})

def descargar_manual(request, documento_id):
    documento = get_object_or_404(Documento, id=documento_id)
    respuesta = requests.get(documento.url_origen)
    if respuesta.status_code == 200:
        ruta_archivo = f'media/biblioteca/{documento.titulo}.pdf'
        with open(ruta_archivo, 'wb') as archivo:
            archivo.write(respuesta.content)
        documento.archivo = f'biblioteca/{documento.titulo}.pdf'
        documento.estado = 'exitoso'
        documento.save()
        return HttpResponse("Descarga completada con éxito.")
    else:
        documento.estado = 'fallido'
        documento.save()
        return HttpResponse("Error al descargar el archivo.", status=400)
    
    
def lista_documentos(request):
    documentos = Documento.objects.all()
    return render(request, 'biblioteca/lista_documentos.html', {'documentos': documentos})

@login_required
def biblioteca_view(request):
    comunidad_id = request.session['comunidad_id']
    
    if not comunidad_id:
        return HttpResponse("Comunidad ID no está presente en la sesión.", status=400)
    
    comunidad = get_object_or_404(Comunidad, id=comunidad_id)
    
    # Recupera los archivos ordenados por el campo "tipo"
    archivos = Archivo.objects.filter(comunidad=comunidad)  # Filtra por la comunidad actual
    return render(request, 'biblioteca/biblioteca.html', {'archivos': archivos, 'comunidad_id': comunidad_id})

@login_required
def biblioteca_archivos(request, comunidad_id=None):
    """
    Vista para mostrar los archivos de una comunidad específica.
    Si no se proporciona `comunidad_id`, se utiliza la primera comunidad asociada al usuario.
    """
    # Obtener la comunidad actual según el ID proporcionado o la primera comunidad asociada al usuario
    if comunidad_id:
        comunidad_actual = get_object_or_404(Comunidad, pk=comunidad_id)
    else:
        comunidad_actual = request.user.comunidades_administradas.first()
        if not comunidad_actual:
            # Mensaje de error si no hay comunidades asociadas
            messages.error(request, "No tienes una comunidad asociada.")
            return redirect("seguimientodocumentos:comunidades")  # Cambiar a la vista apropiada

    # Verificar que el usuario pertenece a la comunidad actual
    if not request.user.comunidades_administradas.filter(pk=comunidad_actual.pk).exists():
        messages.error(request, "No tienes acceso a esta comunidad.")
        return redirect("seguimientodocumentos:comunidades")  # Cambiar a la vista apropiada

    # Filtrar los archivos de la comunidad actual y excluir los registros sin archivo asociado
    archivos = Archivo.objects.filter(comunidad=comunidad_actual).exclude(documento="")

    # Preparar el contexto para la plantilla
    context = {
        'archivos': archivos,
        'comunidad': comunidad_actual,
        'comunidad_id': comunidad_actual.id,  # Garantizar que comunidad_id esté definido
    }

    return render(request, 'biblioteca/biblioteca.html', context)


@login_required
def detalle_archivo(request, id):
    archivo = get_object_or_404(Documento, id=id)
    return render(request, 'detalle_archivo.html', {'archivo': archivo})

def descargar_archivo_externo(request, url):
    response = requests.get(url)
    if response.status_code == 200:
        filename = url.split("/")[-1]
        file_content = response.content

        response = HttpResponse(file_content, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    else:
        return HttpResponse("Error al descargar el archivo", status=404)


@login_required    
def subir_archivo(request):
    comunidad_id = request.session.get('comunidad_id')
    
    if not comunidad_id: # Manejar el caso donde comunidad_id no está en la sesión 
        return HttpResponse("Comunidad ID no está presente en la sesión.", status=400)
    
    
        # Obtener la comunidad y verificar que el usuario pertenece a ella
    comunidad = get_object_or_404(Comunidad, pk=comunidad_id)
    #if comunidad not in request.user.comunidades.all():
        #return HttpResponseForbidden("No tienes una comunidad asociada.")
    
    # Manejar el formulario de subida de archivo
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.comunidad = comunidad
            obj.save()
            
            # Usar namespace para redirigir
            return redirect('biblioteca:biblioteca_archivos', comunidad_id)  
    else:
        form = ArchivoForm()

    # Renderizar la plantilla con el formulario
    return render(request, 'biblioteca/subir_archivo.html', {
        'form': form,
        'comunidad_id': comunidad_id,
    })
    
    # Vista para descargar un archivo
def descargar_archivo(request, id):
    # Buscar el archivo por su id
    archivo = get_object_or_404(Archivo, id=id)

    # Devolver el archivo como una respuesta para la descarga
    response = FileResponse(archivo.documento, as_attachment=True)
    return response 
    # Vista para descargar un archivo
def descargar_archivo(request, id):
    # Buscar el archivo por su id
    archivo = get_object_or_404(Archivo, id=id)

    # Devolver el archivo como una respuesta para la descarga
    response = FileResponse(archivo.documento, as_attachment=True)
    return response

def home(request):
    return render(request, 'home.html')

@login_required
def eliminar_archivo(request, archivo_id):
    archivo = get_object_or_404(Archivo, id=archivo_id)
    comunidad_id = archivo.comunidad_id  # O de dónde provenga este dato
    archivo.delete()
    return redirect('biblioteca:biblioteca_archivos', comunidad_id=comunidad_id)


def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')
        
        # Cuerpo del correo
        asunto = f'Nuevo mensaje de contacto de {nombre}'
        cuerpo = f'Nombre: {nombre}\nCorreo: {email}\n\nMensaje:\n{mensaje}'
        
        try:
            send_mail(
                asunto,  # Asunto del correo
                cuerpo,  # Cuerpo del correo
                settings.DEFAULT_FROM_EMAIL,  # Debe coincidir con EMAIL_HOST_USER
                ['contacto@manon.cl'],  # Correo al que llega el mensaje
                fail_silently=False,
            )
        # Aquí puedes agregar lógica adicional, como enviar un correo electrónico.
            messages.success(request, '¡Gracias por tu mensaje! Nos pondremos en contacto contigo pronto.')
        except Exception as e:
            messages.error(request, f'Ocurrió un error: {e}')
        return redirect('biblioteca:contacto')
    return render(request, 'biblioteca/contacto.html')


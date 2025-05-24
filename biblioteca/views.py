from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse, HttpResponseForbidden,Http404
from biblioteca.models import Documento
import requests
from .models import Documento, Archivo # Asegúrate de tener un modelo Archivo definido
from Aplicaciones.seguimientodocumentos.models import Comunidad
from .forms import ArchivoForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from Aplicaciones.seguimientodocumentos.context_processors import comunidad_context_processor


# Create your views here.


@login_required
def biblioteca_detalle(request, pk):
    proc_ctx = comunidad_context_processor(request)
    comunidad = proc_ctx.get('comunidad')
    if not comunidad:
        raise Http404("Selecciona primero una comunidad válida.")
    
    # Obtén el documento y asegúrate de que pertenece a la comunidad
    documento = get_object_or_404(Documento, pk=pk, comunidad=comunidad)
    return render(request, 'biblioteca/detalle.html', {'documento': documento})

def descargar_manual(request, documento_id):
    # 1) Validar comunidad actual
    proc = comunidad_context_processor(request)
    comunidad = proc.get('comunidad')
    if not comunidad:
        raise Http404("Selecciona primero una comunidad.")
    
    # 2) Recuperar el Documento asegurándote que pertenece a esa comunidad
    documento = get_object_or_404(Documento, id=documento_id, comunidad=comunidad)
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
    
    
@login_required
def biblioteca_archivos(request, comunidad_id=None):
    # 1) Obtener comunidad desde el context processor
    proc_ctx = comunidad_context_processor(request)
    comunidad = proc_ctx.get('comunidad')
    if not comunidad:
        raise Http404("Selecciona primero una comunidad válida.")
    
    # 2) Si pasaron un comunidad_id en la URL, confírmalo
    if comunidad_id is not None and comunidad.id != int(comunidad_id):
        raise Http404("No tienes acceso a esta comunidad.")
    
    # 3) Filtrar los archivos de esta comunidad y excluir sin documento
    archivos = Archivo.objects.filter(comunidad=comunidad).exclude(documento="")

    # 4) Renderizar plantilla con resultados
    return render(request, 'biblioteca/biblioteca.html', {
        'archivos': archivos,
        'comunidad': comunidad,
    })

@login_required
def subir_archivo(request, comunidad_id):
    # 1) Recupera la comunidad o devuelve 404
    comunidad = get_object_or_404(Comunidad, pk=comunidad_id)

    # 2) (Opcional) Verifica que el usuario tenga acceso a esta comunidad
    # if not request.user.comunidades.filter(pk=comunidad_id).exists():
    #     return HttpResponseForbidden("No tienes permiso sobre esta comunidad.")

    # 3) Procesa el formulario de subida de archivo
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.save(commit=False)
            archivo.comunidad = comunidad
            archivo.save()
            # 4) Redirige de vuelta al listado de archivos de esta comunidad
            return redirect('biblioteca:biblioteca_archivos', comunidad_id=comunidad.id)
    else:
        form = ArchivoForm()

    # 5) Renderiza la plantilla pasando el form y la comunidad
    return render(request, 'biblioteca/subir_archivo.html', {
        'form': form,
        'comunidad': comunidad,
    })
    
@login_required    
def descargar_archivo(request, archivo_id):
    """
    Descarga un archivo que el usuario subió a la biblioteca de su comunidad.
    """
    # 1) Obtener comunidad desde el context processor
    ctx = comunidad_context_processor(request)
    comunidad = ctx.get('comunidad')
    if not comunidad:
        raise Http404("Selecciona primero una comunidad válida.")
    
    # 2) Recuperar el Archivo, verificando comunidad
    archivo = get_object_or_404(Archivo, id=archivo_id, comunidad=comunidad)

    # 3) Devolver el fichero como descarga
    #    suponiendo que 'documento' es el FileField de tu modelo Archivo
    response = FileResponse(archivo.documento.open('rb'),
                            as_attachment=True,
                            filename=archivo.documento.name.split('/')[-1])
    
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


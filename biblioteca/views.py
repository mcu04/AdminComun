from django.shortcuts import render, redirect, get_object_or_404
from .models import Documento
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from biblioteca.models import Documento
import requests
from .models import Documento, Archivo  # Asegúrate de tener un modelo Archivo definido
from .forms import ArchivoForm


# Create your views here.

@login_required
def biblioteca_lista(request):
    documentos = Documento.objects.all()
    return render(request, 'biblioteca/lista.html', {'documentos': documentos})
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
    # Recupera los archivos ordenados por el campo "tipo"
    archivos = Archivo.objects.all()
    return render(request, 'biblioteca/biblioteca.html', {'archivos': archivos})

def biblioteca_archivos(request):
    # Obtener todos los documentos desde la base de datos
    archivos = Documento.objects.all()  # Obtén todos los documentos
    return render(request, 'biblioteca/biblioteca.html', {'archivos': archivos})

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
    
def subir_archivo(request):
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('biblioteca:biblioteca')  # Redirige a la página de biblioteca
    else:
        form = ArchivoForm()
    return render(request, 'biblioteca/subir_archivo.html', {'form': form})

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
    archivo.delete()
    return redirect('biblioteca:biblioteca')


# from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
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
import pandas as pd
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from Aplicaciones.seguimientodocumentos.models import seguimiento,documentacion
from django.http import HttpResponseRedirect


    # Create your views here.

def home(request):
    return render(request, "home.html")

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
                return redirect('seguimientodocumentos:listar_seguimiento')
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
        username = request.POST.get('Usuario')  # El nombre del input del formulario debe coincidir
        password = request.POST.get('password')
        remember_me = request.POST.get("remember")  # Para "recordarme" la sesión

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Configurar la expiración de la sesión
            if not remember_me:
                request.session.set_expiry(0)  # Cerrar sesión al cerrar el navegador
            else:
                request.session.set_expiry(1209600)  # 2 semanas

            # Redireccionar a la URL siguiente o a la página de inicio
            next_url = request.POST.get("next", "home")
            return redirect(next_url)
        else:
            # Si la autenticación falla
            return render(request, "iniciar_sesion.html", {
                'error': 'Usuario o contraseña incorrecta'
            })

    # Si el método es GET, renderizar la plantilla de inicio de sesión
    return render(request, "iniciar_sesion.html")
def pagina_inicio(request):
        return render(request, 'inicio.html')  # Cambia a tu plantilla deseada
    
def pagina_principal(request):
    return render(request, 'pagina_principal.html')



def exportar_excel(request):
    # Recupera datos del modelo
    seguimientos = seguimiento.objects.select_related('documentacion').all().values(
        'documentacion__tipo',  # Accede a 'tipo' de documentacion
        'documentacion__categoria',  # Accede a 'categoria' de documentacion
        'documentacion__titulo_documento',  # Accede a 'titulo_documento' de documentacion
        'existe', 
        'observaciones', 
        'fecha_actualizado'
    )

    # Convierte los datos a DataFrame
    df = pd.DataFrame(list(seguimientos))

    # Crea la respuesta HTTP con el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="seguimientos_actualizados.xlsx"'

    # Escribe el DataFrame en el archivo
    df.to_excel(response, index=False)

    return response

def importar_excel(request):
    if request.method == 'POST' and request.FILES.get('archivo_excel'):
        archivo_excel = request.FILES['archivo_excel']

        try:
            # Lee el archivo Excel en un DataFrame
            df = pd.read_excel(archivo_excel)

            # Renombra columnas si es necesario
            df = df.rename(columns={
                'documentacion': 'titulo_documento'
            })

            # Verifica y completa columnas faltantes
            if 'tipo' not in df.columns:
                df['tipo'] = 'Desconocido'
            if 'categoria' not in df.columns:
                df['categoria'] = 'General'

            # Itera sobre las filas y actualiza la base de datos
            for _, row in df.iterrows():
                # Verifica si el documento ya existe en la base de datos o crea uno nuevo
                documento = documentacion.objects.get_or_create(
                    titulo_documento=row['titulo_documento'],
                    defaults={'tipo': row['tipo'], 'categoria': row['categoria']}
                )[0]
                # Crea o actualiza los registros de seguimiento
                seguimiento.objects.update_or_create(
                    documentacion=documento,
                    titulo_documento=row['titulo_documento'],
                    defaults={
                        'existe': True if row['existe'] == 'Si' else False,
                        'observaciones': row['observaciones'] if pd.notnull(row['observaciones']) else '',
                        'fecha_actualizado': row['fecha_actualizado'] if pd.notnull(row['fecha_actualizado']) else None
                    }
                )

            messages.success(request, "Datos importados correctamente.")
        except Exception as e:
            messages.error(request, f"Error al importar: {str(e)}")

        return redirect('importar_excel')

    return render(request, 'importar_excel.html')
        

def exportar_pdf(request):
    # Crear una respuesta tipo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_seguimientos.pdf"'

    # Crear el PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Títulos del informe
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 50, "Listado de Seguimientos Actualizados")

    # Encabezados de la tabla
    encabezados = ["Tipo", "Categoría", "Título Documento", "Existe", "Observaciones", "Fecha Actualizado"]
    p.setFont("Helvetica-Bold", 10)
    y = height - 80
    for i, encabezado in enumerate(encabezados):
        p.drawString(50 + (i * 100), y, encabezado)

    # Datos del modelo
    items = seguimiento.objects.all()
    p.setFont("Helvetica", 9)
    y -= 20

    for item in items:
        datos = [
            getattr(item, 'tipo', 'Sin Tipo') or 'Sin Tipo',
            getattr(item, 'categoria', 'Sin Categoría') or 'Sin Categoría',
            getattr(item, 'titulo_documento', 'Sin Título') or 'Sin Título',
            "Sí" if item.existe else "No",
            item.observaciones or "Sin Observaciones",
            item.fecha_actualizado.strftime("%Y-%m-%d") if item.fecha_actualizado else "Sin Fecha"
        ]

        for i, dato in enumerate(datos):
            p.drawString(50 + (i * 100), y, str(dato))
        y -= 15  # Espaciado entre filas

        # Controlar salto de página
        if y < 50:
            p.showPage()
            y = height - 80
            p.setFont("Helvetica", 9)

    p.save()
    return response

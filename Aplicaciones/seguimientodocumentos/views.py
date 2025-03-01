# from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.timezone import now
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.db.models import Q
from django.db import models
from django.db import IntegrityError
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # Importar paginador
from django.core.mail import send_mail, BadHeaderError
from smtplib import SMTPException
from django.template.loader import render_to_string
from django.conf import settings
from Aplicaciones.seguimientodocumentos.forms import SeguimientoForm   # Crearás este formulario
from Aplicaciones.seguimientodocumentos.forms import RegistroForm, DocumentacionForm, ComunidadForm  
from Aplicaciones.seguimientodocumentos.models import Documentacion, Seguimiento, Comunidad
from urllib.parse import urlencode
import pandas as pd
from io import BytesIO
from openpyxl.styles import Font, Alignment
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.units import inch
import logging
from biblioteca.models import Archivo, Documento
from datetime import datetime
from django.conf import settings


    # Create your views here.

def home(request):
    return render(request, "home.html")

@login_required 
def detallesseguimiento(request, seguimiento_id): 
    seguimiento_instance = get_object_or_404(Seguimiento, pk=seguimiento_id)
    
    if request.method == 'POST':
        form = SeguimientoForm(request.POST, instance=seguimiento_instance) 
        if form.is_valid(): 
            seguimiento_actualizado = form.save(commit=False)
            if seguimiento_actualizado.existe == 'Si': 
                seguimiento_actualizado.fecha_actualizado = now().date()         
            seguimiento_actualizado.save()
            
            return redirect('seguimientodocumentos:listar_seguimiento', 
                    comunidad_id=seguimiento_instance.comunidad.id) 
        else: 
            return render(request, 'detalle_seguimiento.html', { 
                'seguimiento': seguimiento_instance, 
                'form': form, 
                'error': 'Error al actualizar los datos' 
            }) 
    else: 
        form = SeguimientoForm(instance=seguimiento_instance) 
        return render(request, 'detalle_seguimiento.html', { 
            'seguimiento': seguimiento_instance, 
            'form': form 
            })

@login_required
def editar_seguimiento(request, seguimiento_id):
    # Obtener el objeto seguimiento, asegurándose de que pertenezca al usuario autenticado
    seguimiento = get_object_or_404(Seguimiento, pk=seguimiento_id, user=request.user)

    if request.method == "POST":
        # Manejo del formulario en caso de POST
        form = SeguimientoForm(request.POST, instance=seguimiento)
        if form.is_valid():
            form.save()
            
            # Mensaje de éxito y redirección a la vista listar_seguimiento
            messages.success(request, "El seguimiento fue actualizado correctamente.")
            return redirect('seguimientodocumentos:listar_seguimiento', comunidad_id=seguimiento.comunidad.id)
    else:
        # Mostrar el formulario prellenado con la instancia de seguimiento
        form = SeguimientoForm(instance=seguimiento)
        
    # Contexto para la plantilla
    context = {
        'form': form,
        'seguimiento': seguimiento,
        'comunidad_id': seguimiento.comunidad.id,
    }
    return render(request, 'seguimientodocumentos/editar_seguimiento.html', context)

    
@login_required
def seguimiento_pendientes(request, comunidad_id=None):
        # Verificar si `comunidad_id` está presente como argumento
    if not comunidad_id:
        # Intentar obtenerlo de la sesión
        comunidad_id = request.session.get('comunidad_id')
        if not comunidad_id:
            logging.error(f"comunidad_id no encontrado para el usuario {request.user}")
            # Redirigir a una página de error o mensaje
            return redirect('error_page')  # Cambia 'error_page' por la vista que maneje este caso
        
        # Obtener la comunidad o devolver 404 si no existe
    comunidad = get_object_or_404(Comunidad, pk=comunidad_id)
    
    # Guardar el `comunidad_id` en la sesión
    request.session['comunidad_id'] = comunidad_id

    # Obtener el parámetro de búsqueda
    query = request.GET.get('q', '').strip()  # Limpiar espacios en blanco
    
    # Filtrar los seguimientos pendientes
    seguimientos = Seguimiento.objects.filter(
        comunidad=comunidad,  # Filtrar por comunidad
        user=request.user,    # Filtrar por usuario actual
        existe='No'           # Documentos que no existen
    )
    # Si hay una búsqueda, filtrar también por título del documento
    if query:
        seguimientos = seguimientos.filter(
            documentacion__titulo_documento__icontains=query
        )
    
    # Ordenar los resultados
    seguimientos = seguimientos.order_by('-fecha_registrado')
    # Configurar paginación
    paginator = Paginator(seguimientos, 10)  # Mostrar 10 elementos por página
    page_number = request.GET.get('page')
    seguimientos_page = paginator.get_page(page_number)
    
    # Preparar el contexto
    context = {
        'comunidad': comunidad,
        'seguimientos_page': seguimientos_page,  # Página de resultados
        'query': query,  # Query para mantener la búsqueda
    }
    
    # Imprimir IDs en consola para debugging
    for seguimiento in seguimientos_page:
        print(seguimiento.id)
        
    # Renderizar la plantilla
    return render(request, 'seguimientodocumentos/seguimiento_pendiente.html', context)
        

@login_required    
def eliminar_seguimiento(request, seguimiento_id):
        # Obtener el objeto seguimiento, asegurándose de que pertenezca al usuario autenticado
        seguimiento = get_object_or_404(Seguimiento, pk=seguimiento_id, user=request.user)
        
        if request.method == 'POST':
            # Eliminar el seguimiento y redirigir a la lista de seguimientos
            seguimiento.delete()
            
            messages.success(request, "El seguimiento fue eliminado correctamente.")
            
            # Redirige pasando el parámetro comunidad_id
            return redirect('seguimientodocumentos:listar_seguimiento', comunidad_id=seguimiento.comunidad.id)
        
        # Contexto para confirmar la eliminación
        context = {
        'seguimiento': seguimiento,
    }
        
        # Renderiza una página de confirmación para la eliminación
        return render(request, 'seguimientodocumentos/confirmar_eliminar.html', context)

@login_required
def crear_registro(request, modelo_form, template_name, redirect_url):
    """
    Vista generalizada para crear registros.
    Parámetros:
    - modelo_form: Formulario del modelo específico.
    - template_name: Nombre del template a renderizar.
    - redirect_url: URL a la que redireccionar después de guardar.
    """
    if request.method == 'GET':
        form = modelo_form()
        return render(request, template_name, {'form': form})

    else:
        form = modelo_form(request.POST)
        if form.is_valid():
            try:
                nuevo_registro = form.save(commit=False)
                nuevo_registro.save()
                return redirect(redirect_url)  # Redirige a la página correspondiente
            except Exception as e:
                import logging
                logging.error(f"Error al guardar el registro: {e}")
                return render(request, template_name, {
                    'form': form,
                    'error': f'Error al guardar el registro: {str(e)}',
                })
        else:
            return render(request, template_name, {
                'form': form,
                'error': 'Formulario no válido. Por favor, verifica los datos.',
            })

@login_required
def crear_seguimiento(request, comunidad_id):
    # Validar que 'comunidad_id' esté presente
    if not comunidad_id:
        logging.error(f"comunidad_id no proporcionado en la URL para el usuario {request.user}")
        return redirect('error_page')  # Redirigir si no se encuentra 'comunidad_id'

    # Verificar si la comunidad existe
    comunidad = get_object_or_404(Comunidad, pk=comunidad_id)

    if request.method == 'GET':
        form = SeguimientoForm()
        return render(request, 'crear_seguimiento.html', {'form': form, 'comunidad_id':comunidad_id})

    elif request.method == 'POST':
        form = SeguimientoForm(request.POST)
        
        if form.is_valid():
            # Normalizar el campo 'existe' para asegurar consistencia
            existe_normalizado = form.cleaned_data['existe'].strip().capitalize()
            documentacion = form.cleaned_data['documentacion']  # Ajusta según el tipo de relación
            
            # Verificar si ya existe un seguimiento duplicado
            existe_seguimiento = Seguimiento.objects.filter(
                comunidad=comunidad,
                documentacion=documentacion,
                # Agrega más campos aquí si es necesario para determinar duplicados
            ).exists()

            if existe_seguimiento:
                # Mostrar un mensaje de error si ya existe un seguimiento duplicado
                messages.error(request, 'Ya existe un seguimiento con los mismos datos. No se puede duplicar.')
                return render(request, 'crear_seguimiento.html', {
                    'form': form,
                    'comunidad_id': comunidad_id
                })
            try:
                # Crear un nuevo seguimiento pero no guardarlo aún
                nuevo_seguimiento = form.save(commit=False)
                nuevo_seguimiento.user = request.user  # Asigna el usuario actual
                nuevo_seguimiento.comunidad = comunidad  # Asocia el seguimiento con la comunidad
                nuevo_seguimiento.existe = existe_normalizado

                # Establecer fecha_actualizado si el documento existe
                if nuevo_seguimiento.existe == 'Si':
                    nuevo_seguimiento.fecha_actualizado = now().date()

                # Guardar el seguimiento
                nuevo_seguimiento.save()

                # Agregar mensaje de éxito
                
                messages.success(request, 'El seguimiento se ha creado exitosamente.')
                if nuevo_seguimiento.existe == 'Si':
                    return redirect('seguimientodocumentos:listar_seguimiento', comunidad_id=comunidad_id)
                else:
                    return redirect('seguimientodocumentos:seguimiento_pendientes', comunidad_id=comunidad_id)
                
            except IntegrityError as e:
                # Loguear el error en la consola o archivo
                logging.error(f"Error al guardar el seguimiento: {e}")
                messages.error(request, 'Ocurrió un error al guardar el seguimiento. Por favor, intenta nuevamente.')
                return render(request, 'crear_seguimiento.html', {
                    'form': form,
                    'comunidad_id': comunidad_id
                })
        else:
            # Si el formulario no es válido, mostrar un mensaje de error
                messages.error(request, 'Formulario no válido. Por favor, verifica los datos ingresados.')
                return render(request, 'crear_seguimiento.html', {
                'form': form,
                'comunidad_id': comunidad_id
            })

    
@login_required
def crear_documentacion(request):
    return crear_registro(
        request=request,
        modelo_form=DocumentacionForm,
        template_name='crear_documentacion.html',
        redirect_url='seguimientodocumentos:documentos_lista'
    )
                
        
@login_required
def listar_seguimiento(request, comunidad_id):
    # Obtener la comunidad seleccionada o devolver 404 si no existe
    comunidad = get_object_or_404(Comunidad, pk=comunidad_id)
    request.session['comunidad_id'] = comunidad_id  # Guardar comunidad en sesión
    
    # Obtener el query de búsqueda
    query = request.GET.get('q', '').strip()
    
    # Filtrar seguimientos según la comunidad, usuario y otros criterios
    seguimientos = Seguimiento.objects.filter(
        comunidad=comunidad, existe='Si', user=request.user
    )
    
    # Aplicar filtro de búsqueda si se proporciona un query
    if query:
        seguimientos = seguimientos.filter(
            documentacion__titulo_documento__icontains=query
        )
        
        # Ordenar por fecha de actualización
        seguimientos = seguimientos.order_by('-fecha_actualizado')

    # Configurar paginación
    paginator = Paginator(seguimientos, 10)  # Mostrar 10 elementos por página
    page_number = request.GET.get('page')
    seguimientos_page = paginator.get_page(page_number)
    
    # Preparar el contexto
    context = {
        'comunidad': comunidad,
        'seguimientos_page': seguimientos_page,  # Página de resultados
        'query': query,  # Query para mantener la búsqueda
    }
    
    # Imprimir IDs en consola para debugging
    for seguimiento in seguimientos_page:
        print(seguimiento.id)
        
    # Renderizar la plantilla con el contexto
    return render(request, 'seguimientodocumentos/seguimiento.html', context)


@login_required  # Asegura que solo usuarios autenticados accedan
def pagina_inicio(request):
    return render(request, 'inicio.html')  # Cambia a tu plantilla deseada
    
def pagina_principal(request):
    return render(request, 'pagina_principal.html',)



def exportar_excel(request, tipo_seguimiento, comunidad_id=None):
    # Verificar si comunidad_id está presente
    if comunidad_id is None:
        return HttpResponse("Comunidad no especificada.", status=400)

    # Obtener la comunidad o devolver un error si no existe
    comunidad = get_object_or_404(Comunidad, pk=comunidad_id)
    try:
        # Filtrar los datos según el tipo de seguimiento
        if tipo_seguimiento == 'actualizado':
            data = Seguimiento.objects.filter(
            comunidad=comunidad,
            fecha_actualizado__isnull=False
            ).values(
            'fecha_actualizado',  # Campo del modelo Seguimiento
            'documentacion__tipo',  # Campo relacionado del modelo Documentacion
            'documentacion__categoria',  # Campo relacionado del modelo Documentacion
            'documentacion__titulo_documento',  # Campo relacionado del modelo Documentacion
            'existe',  # Campo del modelo Seguimiento
            'observaciones',  # Campo del modelo Seguimiento
            )
            
        elif tipo_seguimiento == 'pendiente':
            data = Seguimiento.objects.filter(
            comunidad=comunidad,
            fecha_actualizado__isnull=True
            ).values(
            'fecha_registrado',  # Campo del modelo Seguimiento
            'documentacion__tipo',  # Campo relacionado del modelo Documentacion
            'documentacion__categoria',  # Campo relacionado del modelo Documentacion
            'documentacion__titulo_documento',  # Campo relacionado del modelo Documentacion
            'existe',  # Campo del modelo Seguimiento
            'observaciones',  # Campo del modelo Seguimiento
            
        )
        else:
            return HttpResponse("Tipo de seguimiento no válido", status=400)
        
        # Verificar si hay datos
        if not data.exists():
            return HttpResponse(f"No se encontraron datos para {tipo_seguimiento} en la comunidad {comunidad.nombre}.", status=404)

        
    # Convertir datos a DataFrame
        df = pd.DataFrame(list(data))
        # Verificar si el DataFrame está vacío
        if df.empty:
            return HttpResponse(f"El DataFrame está vacío para {tipo_seguimiento}", status=404)
        
    # Crear respuesta HTTP
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="seguimiento_{tipo_seguimiento}.xlsx"'

    # Escribir los datos en el archivo Excel
        with BytesIO() as output:
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name=f"Seguimiento_{tipo_seguimiento}")
        
        # Aplicar estilos
                workbook = writer.book
                sheet = writer.sheets[f"Seguimiento_{tipo_seguimiento}"]
                header_format = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#D3D3D3'})
                for col_num, value in enumerate(df.columns.values):
                    sheet.write(0, col_num, value, header_format)
                    sheet.set_column(col_num, col_num, len(value) + 5)
                    
                    # Aplicar formato a las columnas de fecha
                    date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
                if 'fecha_actualizado' in df.columns:
                    fecha_col_idx = df.columns.get_loc('fecha_actualizado')
                    sheet.set_column(fecha_col_idx, fecha_col_idx, 12, date_format)
                if 'fecha_registrado' in df.columns:
                    fecha_col_idx = df.columns.get_loc('fecha_registrado')
                    sheet.set_column(fecha_col_idx, fecha_col_idx, 12, date_format)
        
            # Guardar el archivo Excel en la respuesta
            response.write(output.getvalue())
                
            return response
    except Exception as e:
                return HttpResponse(f"Error al exportar: {str(e)}", status=500)

def iniciar_sesion(request):
    """
    Vista de inicio de sesión:
    - Si el usuario ya está autenticado, redirige a la lista de comunidades.
    - En POST, autentica al usuario y redirige usando el parámetro 'next' (si es válido)
        o, de lo contrario, redirige a la página de comunidades.
    """
    # Si el usuario ya está autenticado, redirige directamente a comunidades
    if request.user.is_authenticated:
        return redirect("seguimientodocumentos:comunidades")
    
    error_msg = None
    
    # Obtener el parámetro 'next' de GET (opcional)
    next_url = request.GET.get("next", "")
    
    # Si next_url contiene "iniciar-sesion", ignóralo para evitar bucles
    if "iniciar-sesion" in next_url:
        next_url = ""

    if request.method == "POST":
        username = request.POST.get("Usuario")
        password = request.POST.get("password")
        # Opcional: manejar "remember me" si el formulario lo incluye
        remember_me = request.POST.get("remember")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Configurar la expiración de la sesión si se selecciona "remember me"
            if remember_me:
                request.session.set_expiry(1209600)  # 2 semanas
            else:
                request.session.set_expiry(0)  # Se cierra la sesión al cerrar el navegador
                
                # Priorizar 'next' desde POST sobre GET
            next_url = request.POST.get("next") or next_url
            
            # Evitar redirigir al login
            if next_url and "iniciar-sesion" not in next_url:
                return redirect(next_url)
            return redirect("seguimientodocumentos:comunidades")
        else:
            error_msg = "Usuario o contraseña incorrecta."
            
            # Renderiza la página de inicio de sesión con cualquier mensaje de error
    return render(request, "iniciar_sesion.html", {"error": error_msg})

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
    return redirect(f"{reverse('seguimientodocumentos:iniciar_sesion')}?{query_string}")
                
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
                documento = Documentacion.objects.get_or_create(
                    titulo_documento=row['titulo_documento'],
                    defaults={'tipo': row['tipo'], 'categoria': row['categoria']}
                )[0]
                # Crea o actualiza los registros de seguimiento
                Seguimiento.objects.update_or_create(
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
        
def generar_tabla_pdf(data, tipo_seguimiento):
    estilos = getSampleStyleSheet()
    estilo_parrafo = estilos["BodyText"]
    estilo_parrafo.wordWrap = 'CJK'
    encabezados = ["Fecha", "Tipo", "Categoría", "Título Documento", "Existe", "Observaciones" ]

    # Formatear filas
    tabla_data = [encabezados]
    for item in data:
        
        # Determinar el valor de "Existe"
        existe_texto = "Sí" if tipo_seguimiento == 'actualizado' and item['existe'] else "No"
        
        # Determinar el valor de "Fecha"
        if tipo_seguimiento == 'actualizado':
            fecha = item['fecha_actualizado'].strftime("%d-%m-%Y") if item['fecha_actualizado'] else "Sin Fecha"
        else:  # Para tipo_seguimiento == 'pendiente'
            fecha = item.get('fecha_registrado', None)
            fecha = fecha.strftime("%d-%m-%Y") if fecha else "Sin Fecha"
        
        fila = [
            fecha,  # Mostrar la fecha correspondiente
            Paragraph(item['documentacion__tipo'] or "Sin tipo", estilo_parrafo),
            Paragraph(item['documentacion__categoria'] or "Sin categoría", estilo_parrafo),
            Paragraph(item['documentacion__titulo_documento'] or "Sin título", estilo_parrafo),
            existe_texto,  # Mostrar "Sí" o "No"
            Paragraph(item['observaciones'] or "Sin Observaciones", estilo_parrafo),
            
        ]
        tabla_data.append(fila)

    ancho_total = letter[0] - (0.5 * inch * 2)  # Ajuste por márgenes
    col_widths = [
        0.10 * ancho_total,  #Fecha
        0.15 * ancho_total,  #Tipo
        0.22 * ancho_total,  #Categoria
        0.25 * ancho_total,  #Titulo Documento
        0.05 * ancho_total,  #Existe
        0.25 * ancho_total,  #Observaciones
    ]

    tabla = Table(tabla_data, colWidths=col_widths)
    estilo_tabla = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    tabla.setStyle(estilo_tabla)
    return tabla

def exportar_pdf(request, tipo_seguimiento, comunidad_id=None):
    # Verificar si comunidad_id está presente
    if comunidad_id is None:
        return HttpResponse("Comunidad no especificada.", status=400)

    # Obtener la comunidad o devolver un error si no existe
    comunidad = get_object_or_404(Comunidad, pk=comunidad_id)

    # Configurar la respuesta como PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="seguimiento_{tipo_seguimiento}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter, leftMargin=0.5 * inch, rightMargin=0.5 * inch)
    elementos = []
    
    # Título
    titulo = f"Listado Seguimiento {'Actualizado' if tipo_seguimiento == 'actualizado' else 'Pendiente'}"
    estilos = getSampleStyleSheet()
    elementos.append(Paragraph(titulo, estilos["Title"]))
    elementos.append(Spacer(1, 0.2 * inch))
    
    # Datos
    if tipo_seguimiento == 'actualizado':
        # Ordenar por `fecha_actualizado` descendente
        data = Seguimiento.objects.filter(
            comunidad=comunidad,
            fecha_actualizado__isnull=False
        ).order_by('-fecha_actualizado').values(
            'documentacion__tipo', 'documentacion__categoria',
            'documentacion__titulo_documento', 'existe',
            'observaciones', 'fecha_actualizado', 'fecha_registrado'
        )
    else:
        # Ordenar por `fecha_registrado` descendente
        data = Seguimiento.objects.filter(
            comunidad=comunidad,
            fecha_actualizado__isnull=True
        ).order_by('-fecha_registrado').values(
            'documentacion__tipo', 'documentacion__categoria',
            'documentacion__titulo_documento', 'existe',
            'observaciones', 'fecha_actualizado', 'fecha_registrado'
        )

    # Generar tabla en PDF
    elementos.append(generar_tabla_pdf(data, tipo_seguimiento))
    
    doc.build(elementos)
    return response

TIPOS_SEGUIMIENTO = {
    'pendiente': True,
    'actualizado': False,
}

def imprimir_seguimientos(request, tipo_seguimiento):
    if tipo_seguimiento not in TIPOS_SEGUIMIENTO:
        raise ValueError("Tipo de seguimiento no válido")
    data = Seguimiento.objects.filter(
        fecha_actualizado__isnull=TIPOS_SEGUIMIENTO[tipo_seguimiento]
    ).values(
        'documentacion__tipo', 'documentacion__categoria',
        'documentacion__titulo_documento', 'existe',
        'observaciones', 'fecha_actualizado'
    )
    return render(request, 'seguimientos/imprimir.html', {'data': data, 'tipo': tipo_seguimiento})


@login_required
def documentacion_list(request):
    comunidad_actual = request.user.comunidades.first()  # Obtener comunidad del usuario
    documentaciones = Documentacion.objects.filter(comunidad=comunidad_actual)
    return render(request, 'documentacion_list.html', {'documentaciones': documentaciones})

@login_required
def documentacion_create(request):
    if request.method == 'POST':
        form = DocumentacionForm(request.POST, user=request.user) # Pasar el usuario autenticado
        if form.is_valid():
            form.save()
            return redirect("seguimientodocumentos:documentacion_list")
    else:
        form = DocumentacionForm(user=request.user)  # Pasar user en GET también
    return render(request, 'documentacion_form.html', {'form': form})

@login_required
def documentacion_edit(request, pk):
    """
    Edita un documento existente.
    """
    documento = get_object_or_404(Documentacion, pk=pk, comunidad__administrador=request.user)

    if request.method == "POST":
        form = DocumentacionForm(request.POST, instance=documento, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('documentacion_list')  # Redirige a la lista de documentos
    else:
        form = DocumentacionForm(instance=documento, user=request.user)  # Carga los datos actuales en el formulario

    return render(request, 'documentacion_form.html', {'form': form, 'editar': True})

@login_required
def documentacion_delete(request, pk):
    """
    Elimina un documento específico con confirmación.
    """
    documento = get_object_or_404(Documentacion, pk=pk, comunidad__administrador=request.user)  # Busca el documento o devuelve 404
    if request.method == "POST":  # Confirmación final antes de eliminar
        documento.delete()
        return redirect('documentacion_list')  # Redirige a la lista después de eliminar

    return render(request, 'documentacion_confirm_delete.html', {'documento': documento})



class DocumentacionListView(LoginRequiredMixin, ListView):
    model = Documentacion
    template_name = 'documentacion_list.html'
    context_object_name = 'documentos'

    def get_queryset(self):
        # Filtrar los documentos solo de las comunidades del administrador logueado
        queryset = Documentacion.objects.filter(comunidad__administrador=self.request.user)
        comunidad_id = self.request.GET.get('comunidad')  # Filtrar por comunidad específica
        if comunidad_id and comunidad_id.isdigit():  # Validar que es un número
            # Filtra solo si la comunidad pertenece al usuario autenticado
            queryset = queryset.filter(comunidad__id=comunidad_id)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lista de comunidades para filtrar
        context['comunidades'] = Comunidad.objects.filter(administrador=self.request.user).only('id', 'nombre')
        return context
    

@login_required
def dashboard(request):
    # Recupera las comunidades asociadas al usuario autenticado
    comunidades = Comunidad.objects.filter(administrador=request.user)
    if not comunidades.exists():
        return redirect('registrar_comunidad')  # Redirige al formulario si no hay comunidades registradas

    context = {
        'usuario': request.user,
        'comunidades': comunidades,
    }
    return render(request, 'dashboard.html', context)

@login_required
def registrar_comunidad(request):
    if request.method == 'POST':
        try:
            form = ComunidadForm(request.POST)
            if form.is_valid():
                # Guardar datos del formulario
                comunidad = form.save(commit=False)
                #administrador = request.POST.get('administrador')  # Capturar el campo personalizado
                comunidad.administrador = request.user  # Asocia al modelo
                comunidad.save()
                
                
                # Agregar documentos iniciales si es necesario
                Documento.objects.create(
                comunidad=comunidad,
                titulo="Documento Inicial",
                descripcion="Descripción del documento inicial."
            )
                Archivo.objects.create(
                comunidad=comunidad,
                titulo_documento="Archivo Inicial",
                tipo="Administracion"
            )
                messages.success(request, f"La comunidad '{comunidad.nombre}' ha sido registrada exitosamente.")
                return redirect('seguimientodocumentos:comunidades')  # Redirige al listado
            else:
                return render(request, 'registrar_comunidad.html', {'form': form, 'error_message': form.errors.as_json(),})
        except Exception as e:
            import traceback
            traceback.print_exc()  # Imprime el stack trace completo en la consola
            return render(request, 'registrar_comunidad.html', {'form': form, 'error_message': str(e)})
    else:
        form = ComunidadForm()
    return render(request, 'registrar_comunidad.html', {'form': form})

def detalles_comunidad(request, comunidad_id):
    comunidad = get_object_or_404(Comunidad, id=comunidad_id)
    return render(request, 'detalles_comunidad.html', {'comunidad': comunidad})

@login_required
def listar_comunidades(request):
    # Ahora request.user será un usuario autenticado, por lo que se puede filtrar sin error
    comunidades = Comunidad.objects.filter(administrador=request.user)
    return render(request, "listar_comunidades.html", {'comunidades': comunidades})

from django.shortcuts import get_object_or_404

@login_required
def actualizar_comunidad(request, pk):
    comunidad = get_object_or_404(Comunidad, pk=pk, administrador=request.user)
    if request.method == 'POST':
        form = ComunidadForm(request.POST, instance=comunidad)
        if form.is_valid():
            form.save()
            return redirect('seguimientodocumentos:comunidades')
        else:
            return render(request, 'actualizar_comunidad.html', {'form': form, 'error_message': form.errors})
    else:
        form = ComunidadForm(instance=comunidad)
    return render(request, 'actualizar_comunidad.html', {'form': form})

@login_required
def eliminar_comunidad(request, pk):
    comunidad = get_object_or_404(Comunidad, pk=pk, administrador=request.user)
    if request.method == 'POST':
        comunidad.delete()
        return redirect('seguimientodocumentos:comunidades')
    return render(request, 'eliminar_comunidad.html', {'comunidad': comunidad})

@login_required
def seleccionar_comunidad(request, comunidad_id):
    """
    Guarda en la sesión la comunidad seleccionada por el usuario
    """
    comunidad = get_object_or_404(Comunidad, id=comunidad_id)

    # Guardamos la comunidad en la sesión
    request.session['comunidad_id'] = comunidad.id
    request.session['comunidad_nombre'] = comunidad.nombre

    # Redirigir a la página de seguimiento o donde corresponda
    return redirect('ruta_donde_redirigir')  # Modificar con la URL correcta





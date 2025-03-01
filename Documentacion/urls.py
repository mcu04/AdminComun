"""
URL configuration for Documentacion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Aplicaciones.seguimientodocumentos import views
from django.conf import settings
from django.conf.urls.static import static
from Aplicaciones.seguimientodocumentos.views import listar_comunidades
from Aplicaciones.seguimientodocumentos import views as seguimiento_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("seguimiento/", include("Aplicaciones.seguimientodocumentos.urls")),  # Incluye las rutas de seguimiento
    path('seguimiento/iniciar-sesion/', include('Aplicaciones.seguimientodocumentos.autenticacion.urls')),  # Ruta de login
    path('biblioteca/', include('biblioteca.urls')),   # Incluir URLs de la biblioteca
    path('', seguimiento_views.iniciar_sesion, name='iniciar_sesion'),
    path('accounts/', include('accounts.urls')),  # Asegúrate de que tu aplicación maneja autenticación
    path('seguimiento/', include('django.contrib.auth.urls')),
    path('comunicacion/', include('comunicacion.urls')),
    
    path('seguimiento/comunidades/', listar_comunidades, name='comunidades'),
    path('mantenimiento/', include('mantenimiento.urls', namespace='mantenimiento')),
    path("autenticacion/", include("Aplicaciones.seguimientodocumentos.autenticacion.urls", namespace="autenticacion")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)








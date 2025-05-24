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
from django.conf import settings
from django.conf.urls.static import static
from Aplicaciones.seguimientodocumentos.autenticacion import views as auth_views
from Aplicaciones.seguimientodocumentos.views import listar_comunidades
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),

    # Rutas de autenticación PERSONALIZADAS bajo /seguimiento/auth/
    path("auth/",include(("Aplicaciones.seguimientodocumentos.autenticacion.urls", "autenticacion"),
            namespace="autenticacion",),
    ),
    # Rutas “puras” de seguimiento (listas, CRUD, etc.)
    path("seguimiento/", include(("Aplicaciones.seguimientodocumentos.urls", "seguimientodocumentos")),
    ),

    # Biblioteca
    path("biblioteca/", include("biblioteca.urls")),

    # Comunicación
    path("comunicacion/", include("comunicacion.urls")),

    # Mantenimiento
    path(
        "mantenimiento/",
        include(("mantenimiento.urls", "mantenimiento"), namespace="mantenimiento"),
    ),

    # **Root**: lo redirigimos directamente a comunidades
    path('', RedirectView.as_view(pattern_name='seguimientodocumentos:comunidades', permanent=False)),

    # Auth genérica de Django (si la necesitas para password_change, etc.)
    path("accounts/", include("django.contrib.auth.urls")),
]

# Sirve estáticos en DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
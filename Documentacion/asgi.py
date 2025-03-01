"""
ASGI config for Documentacion project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from comunicacion_real.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Documentacion.settings')

application = get_asgi_application()




os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comunicacion_condominio.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Maneja solicitudes HTTP normales
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Importa las rutas de WebSocket de la app "comunicacion"
        )
    ),
})

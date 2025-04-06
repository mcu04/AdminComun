import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import mantenimiento.routing 


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Documentacion.settings")
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            mantenimiento.routing.websocket_urlpatterns
        )
    ),
})
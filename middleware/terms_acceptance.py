# middleware/terms_acceptance.py

import logging
from django.shortcuts import redirect
from django.urls import resolve, Resolver404, reverse
from django.db.utils import ProgrammingError, OperationalError
from django.utils.deprecation import MiddlewareMixin
import re

class TermsAcceptanceMiddleware(MiddlewareMixin):
    """
    Middleware que redirige a la vista de Términos y Condiciones a cualquier usuario autenticado
    que no haya aceptado los términos, excepto en ciertas rutas seguras (login, logout, t&c, password reset, etc).
    """

    def process_request(self, request):
        # No interferir si el usuario no está autenticado
        if not request.user.is_authenticated:
            return None

        # Paths que nunca deberían redirigirse
        path = request.path_info
        
        # Ignorar recursos estáticos y media
        if path.startswith('/static/') or path.startswith('/media/'):
            return None
        
        # Construimos reverses solo una vez:
        exempt_urls = {
            reverse('autenticacion:iniciar_sesion'),
            reverse('autenticacion:terminos_condiciones'),
            reverse('autenticacion:cerrar_sesion'),
            reverse('autenticacion:password_reset_request'),
        }
        
        # Ignorar rutas exentas
        if any(path.startswith(url) for url in exempt_urls):
            return None
        
        # Verificamos el perfil del usuario
        profile = getattr(request.user, 'profile', None)
        if not profile or not profile.accepted_terms:
            # Redirigir a T&C con el parámetro next
            return redirect(f"{reverse('autenticacion:terminos_condiciones')}?next={path}")

        # Si ya aceptó términos, dejamos pasar
        return None


from .models import Comunidad

def comunidad_context_processor(request):
    # Por ejemplo, si la comunidad está en la sesión o en el perfil del usuario:
    comunidad = None
    if request.user.is_authenticated:
        comunidad_id = request.session.get('comunidad_id')
        if comunidad_id:
            # Aseguramos que sea una comunidad del usuario
            comunidad = Comunidad.objects.filter(
                pk=comunidad_id,
                administrador=request.user
            ).first()
    return {'comunidad': comunidad}

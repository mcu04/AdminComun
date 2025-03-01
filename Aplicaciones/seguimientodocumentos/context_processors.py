def comunidad_context_processor(request):
    # Por ejemplo, si la comunidad está en la sesión o en el perfil del usuario:
    comunidad = None
    if request.user.is_authenticated:
        comunidad = request.session.get('comunidad')  # o la lógica que uses
    return {'comunidad': comunidad}

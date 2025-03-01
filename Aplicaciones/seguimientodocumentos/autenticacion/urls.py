# autenticacion/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Esto busca el archivo views.py en el mismo directorio

app_name = 'autenticacion'

urlpatterns = [
    # Rutas de autenticación estándar:
    path('login/', auth_views.LoginView.as_view(template_name='iniciar_sesion.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    # Rutas para la recuperación de contraseña personalizada:
    path("password_reset/", views.password_reset_request, name="password_reset_request"),
    path("reset/<uuid:token>/", views.password_reset_confirm, name="password_reset_confirm"),
]





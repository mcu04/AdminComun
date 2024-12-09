# autenticacion/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Esto busca el archivo views.py en el mismo directorio

app_name = 'autenticacion'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='iniciar_sesion.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('registrarse/', views.registrarse, name='registrarse'),
]






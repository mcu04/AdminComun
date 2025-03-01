from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def some_view(request):
    return HttpResponse("Página de autenticación funcionando correctamente")
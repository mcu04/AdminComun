from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'main/home.html')  # Asegúrate de que este archivo existe en templates/main/

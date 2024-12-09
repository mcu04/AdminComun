import requests
from django.core.management.base import BaseCommand
from biblioteca.models import Documento

class Command(BaseCommand):
    help = "Descarga archivos automáticamente desde URLs de organismos externos."

    def handle(self, *args, **kwargs):
        documentos = Documento.objects.all()
        for doc in documentos:
            respuesta = requests.get(doc.url_origen)
            if respuesta.status_code == 200:
                ruta_archivo = f'media/biblioteca/{doc.titulo}.pdf'
                with open(ruta_archivo, 'wb') as archivo:
                    archivo.write(respuesta.content)
                doc.archivo = f'biblioteca/{doc.titulo}.pdf'
                doc.estado = 'exitoso'
                doc.save()
                self.stdout.write(f"Descargado: {doc.titulo}")
            else:
                doc.estado = 'fallido'
                doc.save()
                self.stdout.write(f"Error al descargar: {doc.titulo}")

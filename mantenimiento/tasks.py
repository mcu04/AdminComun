from celery import shared_task
from django.utils import timezone
from .models import MantencionPreventiva
from django.core.mail import send_mail

@shared_task
def enviar_recordatorios():
    hoy = timezone.now().date()
    proximas = MantencionPreventiva.objects.filter(
        fecha_programada__lte=hoy + timezone.timedelta(days=3),
        fecha_realizada__isnull=True
    )
    for mantencion in proximas:
        # Aquí podrías personalizar el asunto, mensaje y destinatarios
        send_mail(
            'Recordatorio de Mantención',
            f'Recuerda que la mantención de {mantencion.instalacion} está programada para {mantencion.fecha_programada}.',
            'from@example.com',
            ['destinatario@example.com'],
        )
    return f'Se han enviado recordatorios para {proximas.count()} mantenciones.'
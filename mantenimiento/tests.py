from django.test import TestCase
from unittest.mock import patch
from datetime import datetime, timedelta
from mantenimiento.models import Mantenimiento

class MantenimientoNotificationTest(TestCase):
    
    def setUp(self):
        """ Configuración inicial para las pruebas """
        # Creamos un objeto Mantenimiento para usarlo en las pruebas
        self.now = datetime.now()
        self.mantenimiento = Mantenimiento.objects.create(
            fecha_inicio=self.now,
            fecha_fin=self.now + timedelta(hours=2),
            descripcion="Prueba de mantenimiento",
            estado="pendiente"
        )

    @patch('mantenimiento.views.send_maintenance_notification')
    def test_iniciar_mantenimiento_sends_notification(self, mock_send_notification):
        """
        Verifica que al llamar a iniciar_mantenimiento se envíe una notificación.
        """
        # Llamamos al método que debería enviar la notificación.
        self.mantenimiento.iniciar_mantenimiento()
        
        # Verificamos que se haya llamado la función de notificación con los parámetros esperados.
        mock_send_notification.assert_called_with(
            self.mantenimiento.descripcion, 
            self.mantenimiento.fecha_inicio, 
            self.mantenimiento.fecha_fin
        )
    
    def test_mantenimiento_creation(self):
        """
        Verifica que el objeto Mantenimiento se haya creado correctamente.
        """
        # Verificamos que el mantenimiento se haya guardado en la base de datos
        mant = Mantenimiento.objects.get(id=self.mantenimiento.id)
        self.assertEqual(mant.descripcion, "Prueba de mantenimiento")
        self.assertEqual(mant.estado, "pendiente")
        self.assertTrue(mant.fecha_inicio <= mant.fecha_fin)
    
    def tearDown(self):
        """ Limpieza después de cada prueba (opcional, si es necesario limpiar los datos) """
        self.mantenimiento.delete()  # Elimina el objeto de prueba si fuera necesario
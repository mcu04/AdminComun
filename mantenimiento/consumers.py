from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
import json
import logging


logger = logging.getLogger(__name__)

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Grupo general de notificaciones
        try: 
            await self.channel_layer.group_add("notifications", self.channel_name)
            await self.accept()
            logger.info("Conexión aceptada para %s", self.channel_name)
        except Exception as e:
            logger.error("Error en la conexión WebSocket: %s", e)
            await self.close()

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard("notifications", self.channel_name)
            logger.info("Desconexión de %s", self.channel_name)
        except Exception as e:
            logger.error("Error al desconectar: %s", e)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get("type", "general")  # Tipo de mensaje (mantenimiento, alerta, etc.)
            message_content = data.get("message", "Mensaje vacío")

            # Personaliza según el tipo de mensaje
            formatted_message = f"[{message_type.upper()}] {message_content}"

        except json.JSONDecodeError as e:
            logger.error("Error al decodificar JSON: %s", e)
            formatted_message = "Error al procesar el mensaje"
        await self.send(text_data=json.dumps({"message": formatted_message}))

    async def send_notification(self, event):
        try:
            await self.send(text_data=json.dumps({
                "message": event["message"]
            }))
        except Exception as e:
            logger.error("Error al enviar notificación: %s", e) 
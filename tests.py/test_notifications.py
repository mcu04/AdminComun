from channels.testing import WebsocketCommunicator
from Documentacion.asgi import application 
import json
import pytest

@pytest.mark.asyncio
async def test_notification_websocket():
    communicator = WebsocketCommunicator(application, "/ws/notifications/")
    connected, _ = await communicator.connect()

    assert connected, "No se pudo conectar el WebSocket"

    # Envía un mensaje simulado desde el servidor
    await communicator.send_json_to({
        "type": "send_notification",
        "message": "Prueba de notificación"
    })

    response = await communicator.receive_json_from()
    
    assert response["message"] == "[SEND_NOTIFICATION] Prueba de notificación"

    await communicator.disconnect()
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_maintenance_notification(message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "maintenance_notifications",
        {
            "type": "send_notification",  # Este tipo hace que se invoque send_notification en el consumer
            "message": message,
        }
    )
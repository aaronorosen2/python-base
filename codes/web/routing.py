from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter

from notifications.consumers import NotificationConsumer

application = ProtocolTypeRouter({
    "websocket": 
        URLRouter([
            # URLRouter just takes standard Django path() or url() entries.
            path("notifications", NotificationConsumer.as_asgi(),name="ws_notifications"),
        ]),
})
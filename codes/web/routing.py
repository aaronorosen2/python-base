from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from notifications.consumers import NotificationConsumer
# from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter({
    # "http": get_asgi_application(),
    "websocket": 
        URLRouter([
            # URLRouter just takes standard Django path() or url() entries.
            # path("notifications/<str:room_name>/", NotificationConsumer.as_asgi(),name="ws_notifications"),
            path("notifications/", NotificationConsumer.as_asgi(),name="ws_notifications"),
            
        ]),
})

# application = ProtocolTypeRouter({

#     "websocket": AuthMiddlewareStack(
#         URLRouter([
#             re_path(r"^notifications/$", NotificationConsumer.as_asgi()),
#         ])
#     ),

# })
import django
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from django.core.asgi import get_asgi_application

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()

from notifications.consumers import NotificationConsumer, NotificationConsumerQueue, VstreamConsumer
from chat.consumers import ChatConsumer
from chat.middleware import WebSocketJWTAuthMiddleware


application = ProtocolTypeRouter({
    # "http": get_asgi_application(),
    "websocket": 
        WebSocketJWTAuthMiddleware(URLRouter([
            # URLRouter just takes standard Django path() or url() entries.
            # path("notifications/<str:room_name>/", NotificationConsumer.as_asgi(),name="ws_notifications"),
            # path("notifications/", NotificationConsumer.as_asgi(),name="ws_notifications"),
            # re_path(r'notifications/(?P<room_name>\w+)/$', NotificationConsumer.as_asgi()),
            # re_path(r'notifications/(?P<room_name>\w+)/$', NotificationConsumerQueue.as_asgi()),
            # re_path(r'vstream/', VstreamConsumer.as_asgi()),
            re_path(r'msg/(?P<user_id>\w+)/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
        ])),
})


# application = ProtocolTypeRouter({

#     "websocket": AuthMiddlewareStack(
#         URLRouter([
#             re_path(r"^notifications/$", NotificationConsumer.as_asgi()),
#         ])
#     ),

# })
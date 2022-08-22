import django
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

from channels.routing import ProtocolTypeRouter, URLRouter

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()

from channels.auth import AuthMiddlewareStack
from ringlessVoiceMail.consumer import RinglessVoiceMailConsumer
from notifications.consumers import ( NotificationConsumer, 
                                    NotificationConsumerQueue, 
                                    VstreamConsumer )
from chat.consumers import ( ChatConsumer, ChatConsumerQueue,
                            MessageUserConsumer,MessageSMSConsumer)
                            
from chat.middleware import WebSocketJWTAuthMiddleware


application = ProtocolTypeRouter({
    # "http": get_asgi_application(),
    "websocket": 
        WebSocketJWTAuthMiddleware(URLRouter([
            # URLRouter just takes standard Django path() or url() entries.
            # path("notifications/<str:room_name>/", NotificationConsumer.as_asgi(),name="ws_notifications"),
            # path("notifications/", NotificationConsumer.as_asgi(),name="ws_notifications"),
            # re_path(r'notifications/(?P<room_name>\w+)/$', NotificationConsumer.as_asgi()),
            re_path(r'notifications/(?P<room_name>\w+)/$', NotificationConsumerQueue.as_asgi()),
            re_path(r'vstream/', VstreamConsumer.as_asgi()),
            re_path(r'msg/channel/$', ChatConsumer.as_asgi()),
            re_path(r'msg/user/$',MessageUserConsumer.as_asgi()),
            re_path(r'msg/sms/$',MessageSMSConsumer.as_asgi()),
        ])),
})


# application = ProtocolTypeRouter({

#     "websocket": AuthMiddlewareStack(
#         URLRouter([
#             re_path(r"^notifications/$", NotificationConsumer.as_asgi()),
#         ])
#     ),

# })
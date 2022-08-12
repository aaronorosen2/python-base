from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from notifications.consumers import NotificationConsumer, NotificationConsumerQueue, VstreamConsumer
from chat.consumers import ChatConsumer,ChatConsumerQueue,MessageUserConsumer
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
            # re_path(r'msg/(?P<receiver_id>\w+)/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
            re_path(r'msg/user/$',MessageUserConsumer.as_asgi()),
            re_path(r'msg/channel/$', ChatConsumer.as_asgi()),
            # re_path(r'msg/sms/$', ChatConsumer.as_asgi()),
            # re_path(r'msg_queue/(?P<user_id>\w+)/(?P<room_name>\w+)/$', ChatConsumerQueue.as_asgi()),

        ])),
})


# application = ProtocolTypeRouter({

#     "websocket": AuthMiddlewareStack(
#         URLRouter([
#             re_path(r"^notifications/$", NotificationConsumer.as_asgi()),
#         ])
#     ),

# })
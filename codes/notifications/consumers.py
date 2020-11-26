from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'users'
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'notification_broadcast',
                'message': text_data,
            },
        )

    async def notification_broadcast(self,event):
        await self.send(text_data=event["message"])

    async def disconnect(self, close_code):
        pass
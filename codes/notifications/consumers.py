from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'users'
        # self.user = self.scope["user"]
        # print(self.user.id)
        # print(self.channel_name)
        # print(self.room_name)
        # print(self.scope['url_route'])
        # print(self.scope['url_route']['kwargs'])
        self.group_name = self.scope['url_route']['kwargs']['user_id']
        print(self.group_name)
        await self.channel_layer.group_add(
            self.room_name,
            self.group_name
        )
        await self.accept()
        # print(self.channel_layer.__dict__)
        # await self.channel_layer.send(
        #     self.room_name,
        #     {
        #         'type': 'users_list',
        #         'message': self.channel_layer.__dict__
        #     }
        # )

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'notification_broadcast',
                'message': text_data,
            },
        )
    
    async def users_list(self,event):
        await self.send_json(
            {
                "msg_type": settings.MSG_TYPE_MESSAGE,
                "channel": event["message"]
            },
        )
    
    async def notification_broadcast(self,event):
        await self.send(text_data=event["message"])

    async def disconnect(self, close_code):
        pass
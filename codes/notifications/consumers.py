from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class NotificationConsumer(AsyncWebsocketConsumer):
    user_dictionary = {}

    def getList(self,dict): 
        list = [] 
        for key in dict.keys(): 
            list.append(key) 
            
        return list

    async def connect(self):
        self.room_name = 'users'
        # self.user = self.scope["user"]
        # print(self.user.id)
        # print(self.channel_name)
        # print(self.room_name)
        # print(self.scope['url_route'])
        # print(self.scope['url_route']['kwargs'])
        self.user_name = self.scope['url_route']['kwargs']['room_name']
        # print(self.user_name)
        self.user_room_name = "notif_room_for_user_" + str(self.user_name)  ##Notification room name
        print(self.user_room_name)
        self.user_dictionary[self.user_name] = self.user_room_name
        print(self.user_dictionary)
        # self.room_group_name = 'chat_%s' % self.room_name
        # await self.channel_layer.group_add(
        #     self.room_name,
        #     self.channel_name,
        #     # self.user_name
        # )
        # self.user = self.scope["user"]

        print(self.room_name)
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        print(self.getList(self.user_dictionary))
        users_list = self.getList(self.user_dictionary)
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'users_list',
                'users': json.dumps({'users':users_list,'action':'users_list'}),
            },
        )
        await self.accept()
        # print(self.channel_layer.__dict__)
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'users_list',
        #         'message': "allusers"
        #     }
        # )

    async def receive(self, text_data):
        # print(self.channel_name)
        # print(self.channel_layer)
        # print(self.user_name)
        # print(text_data)
        # channel_name = self.user_dictionary[]
        # await self.channel_layer.group_add(
        #     self.room_name,
        #     self.channel_name,
        #     # self.user_name
        # )
        print(text_data)
        send_data = json.loads(text_data)
        print(type(send_data))
        print(send_data)
        # await
        if(send_data['action'] == 'solo'):
            reciever = self.user_dictionary[send_data['reciever']]
            print(reciever)
            await self.channel_layer.send(
                self.room_name,
                {
                    'type': 'notification_to_user',
                    'message': text_data,
                },
            )
        else:
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'notification_broadcast',
                    'message': text_data,
                },
            )
    
    async def users_list(self,event):
        print(self.channel_layer)
        await self.send(text_data=event["users"])
        # await self.send(
        #     {
        #         "users": self.user_dictionary
        #     },
        # )
    async def notification_to_user(self,event):
        await self.send(text_data=event["message"])


    async def notification_broadcast(self,event):
        await self.send(text_data=event["message"])

    async def disconnect(self, close_code):
        pass

class NotificationConsumerSync(WebsocketConsumer):
    user_dictionary = {}

    def getList(self,dict): 
        list = [] 
        for key in dict.keys(): 
            list.append(key) 
            
        return list

    def connect(self):
        self.room_name = 'users'
        # self.user = self.scope["user"]
        # print(self.user.id)
        # print(self.channel_name)
        # print(self.room_name)
        # print(self.scope['url_route'])
        # print(self.scope['url_route']['kwargs'])
        self.user_name = self.scope['url_route']['kwargs']['room_name']
        print(self.user_name)
        self.user_dictionary[self.user_name] = self.channel_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )

        print(self.getList(self.user_dictionary))
        users_list = self.getList(self.user_dictionary)
        # await self.channel_layer.group_send(
        #     self.room_name,
        #     {
        #         'type': 'users_list',
        #         'users': json.dumps({'users':users_list,'action':'users_list'}),
        #     },
        # )
        async_to_sync(self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'users_list',
                    'users': json.dumps({'users':users_list,'action':'users_list'}),
                },
            ))
        self.accept()
        # print(self.channel_layer.__dict__)
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'users_list',
        #         'message': "allusers"
        #     }
        # )

    def receive(self, text_data):
        print(self.channel_name)
        print(self.channel_layer)
        print(self.user_name)
        # print(text_data)
        # channel_name = self.user_dictionary[]
        # await self.channel_layer.group_add(
        #     self.room_name,
        #     self.channel_name,
        #     # self.user_name
        # )
        send_data = json.loads(text_data)
        print(send_data)
        if(send_data.action == 'solo'):
            reciever = self.user_dictionary[send_data.reciever]
            print(reciever)
            # await reciever.send(
            #     self.room_name,
            #     {
            #         'type': 'notification_to_user',
            #         'message': text_data,
            #     },
            # )
            async_to_sync(self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'notification_to_user',
                    'message': text_data,
                },
            ))
        else:
            async_to_sync(self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'notification_broadcast',
                    'message': text_data,
                },
            ))
    
    def users_list(self,event):
        print(self.channel_layer)
        self.send(text_data=event["users"])
        # await self.send(
        #     {
        #         "users": self.user_dictionary
        #     },
        # )
    def notification_to_user(self,event):
        self.send(text_data=event["message"])


    def notification_broadcast(self,event):
        self.send(text_data=event["message"])

    def disconnect(self, close_code):
         # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )
        del self.user_dictionary[self.user_name]
        print(self.user_dictionary)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'users_list',
                'users': json.dumps({'users':users_list,'action':'users_list'}),
            }
        )
        # await self.channel_layer.group_send(
        #     self.room_name,
        #     {
        #         'type': 'users_list',
        #         'users': json.dumps({'users':users_list,'action':'users_list'}),
        #     },
        # )
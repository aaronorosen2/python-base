from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class NotificationConsumer(AsyncWebsocketConsumer):
    user_dictionary = {}
    user_name = ""
    user_room_name = ""
    def getList(self,dict): 
        list = [] 
        for key in dict.keys(): 
            list.append(key) 
            
        return list

    async def connect(self):
        self.room_name = 'user'
        # self.user = self.scope["user"]
        # print(self.user.id)
        # print(self.channel_name)
        # print(self.room_name)
        # print(self.scope['url_route'])
        # print(self.scope['url_route']['kwargs'])
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        # # print(self.user_name)
        # self.room_group_name = "sender_" + str(self.room_name)  ##Notification room name
        # # # print(self.room_group_name)
        # self.user_dictionary[self.room_name] = self.room_group_name
        # print(self.user_dictionary)
        # # self.room_group_name = 'chat_%s' % self.room_name
        # await self.channel_layer.group_add(
        #     self.room_name,
        #     self.channel_name,
        #     # self.user_name
        # )
        # # self.user = self.scope["user"]
        #
        # # print(self.room_name)
        # # await self.channel_layer.group_add(
        # #     self.room_group_name,
        # #     self.channel_name
        # # )
        # # # print(self.getList(self.user_dictionary))
        # users_list = self.getList(self.user_dictionary)
        # # # for key, value in self.user_dictionary.items():
        # for key in list(self.user_dictionary.keys()):
        #     # print(key,value)
        #     await self.channel_layer.group_send(
        #         self.user_dictionary[key],
        #         {
        #             'type': 'users_list',
        #             'users': json.dumps({'users': users_list, 'action': 'users_list'}),
        #         },
        #     )
        # for name in users_list:
        #     print(name)
        #     await self.channel_layer.group_send(
        #         "notif_room_for_user_" + str(name),
        #         {
        #             'type': 'users_list',
        #             'users': json.dumps({'users': users_list, 'action': 'users_list'}),
        #         },
        #     )
        #
        # await self.channel_layer.group_send(
        #     "notif_room_for_user_" + str(name),
        #     {
        #         'type': 'users_list',
        #         'users': json.dumps({'users': users_list, 'action': 'users_list'}),
        #     },
        # )
        # await self.channel_layer.group_add(
        #     self.room_name,
        #     self.channel_name
        # )
        from channels.layers import get_channel_layer

        channel_layer = get_channel_layer()
        print(channel_layer)
        await channel_layer.send("channel_name", {
            "type": "chat.message",
            "text": "Hello there!",
        })
        # print(self.channel_name)
        # await self.channel_layer.send(self.channel_name, {
        #     "type": "chat_message",
        #     "text": "Hello there!",
        # })
        await self.accept()
        
        # print(self.channel_layer)
        
        # print(self.channel_layer.__dict__)
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'users_list',
        #         'message': "allusers"
        #     }
        # )
    # async def send(self, text_data=None, bytes_data=None, close=False):
    #     """
    #     Sends a reply back down the WebSocket
    #     """
    #     if text_data is not None:
    #         await super().send({"type": "websocket.send", "text": text_data})
    #     elif bytes_data is not None:
    #         await super().send({"type": "websocket.send", "bytes": bytes_data})
    #     else:
    #         raise ValueError("You must pass one of bytes_data or text_data")
    #     if close:
    #         await self.close(close)
    async def chat_message(self, event):
        # Handles the "chat.message" event when it's sent to us.
        self.send(text_data=event["text"])

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
        # print(text_data)
        send_data = json.loads(text_data)

        # print(type(send_data))
        # print(send_data)
        # await
        if(send_data['action'] == 'store_user_name'):
            self.room_name = send_data['user_name']
            self.user_name = send_data['user_name']
            self.user_room_name = "notif_room_for_user_" + str(self.user_name)
            # self.room_group_name = "notif_room_for_user_" + str(self.room_name)  ##Notification room name
            # print(self.room_group_name)
            # print(self.channel_layer)
            self.user_dictionary[self.user_name] = self.user_room_name
            # print(self.channel_name)
            await self.channel_layer.group_add(
                self.user_room_name,
                self.channel_name
            )
            users_list = self.getList(self.user_dictionary)
            # print(users_list)
            for key in users_list:
                # print(key)
                await self.channel_layer.group_send(
                    self.user_dictionary[key],
                    {
                        'type': 'users_list',
                        'users': json.dumps({'users': users_list, 'action': 'users_list'}),
                    },
                )
        if(send_data['action'] == 'solo'):
            reciever = self.user_dictionary[send_data['reciever']]
            # print(reciever)
            del send_data['reciever']
            # message = send_data['message']
            await self.channel_layer.group_send(
                reciever,
                {
                    'type': 'notification_to_user',
                    'message': json.dumps(send_data),
                },
            )
        elif(send_data['action'] == 'broadcast'):
            users_list = self.getList(self.user_dictionary)
            for user in users_list:
                await self.channel_layer.group_send(
                    self.user_dictionary[user],
                    {
                        'type': 'notification_broadcast',
                        'message': text_data,
                    },
                )
    
    async def users_list(self,event):
        # print(self.channel_layer)
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
        print("Disconnect!!!!")
        # await self.channel_layer.group_discard(
        #     self.room_group_name,
        #     self.channel_name
        # )
        
        print(close_code)
        await self.close()
        if(self.user_name in self.user_dictionary):
            print(self.user_dictionary[self.user_name])
            print(self.room_name)
            # print(self.user_name)
            del self.user_dictionary[self.user_name]
            print(self.user_dictionary)
            users_list = self.getList(self.user_dictionary)
            await self.channel_layer.group_discard(
                self.user_dictionary[self.user_name],
                self.channel_name
            )
            print(users_list)
            for key in users_list:
                # print(key)
                await self.channel_layer.group_send(
                    self.user_dictionary[key],
                    {
                        'type': 'users_list',
                        'users': json.dumps({'users': users_list, 'action': 'users_list'}),
                    },
                )

        # print(close_code)
        # print(self.user_dictionary[self.room_name])
        # del self.user_dictionary[self.room_name]

from channels.layers import get_channel_layer
# from channels import Clients

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        # Make a database row with our channel name
        async_to_sync(self.channel_layer.send(
            self.channel_name,
            {
                'type': 'chat_message',
                'users': json.dumps({'users':users_list,'action':'users_list'}),
            },
        ))
        # Clients.objects.create(channel_name=self.channel_name)
        # print(Clients.objects.all())

    def disconnect(self, close_code):
        # Note that in some rare cases (power loss, etc) disconnect may fail
        # to run; this naive example would leave zombie channel names around.
        # Clients.objects.filter(channel_name=self.channel_name).delete()
        pass

    # def receive(self, text_data):
    #     channel_layer = get_channel_layer()

    #     async_to_sync(self.channel_layer.send(
    #         self.room_name,
    #         {
    #             'type': 'users_list',
    #             'users': json.dumps({'users':users_list,'action':'users_list'}),
    #         },
    #     ))

    def chat_message(self, event):
        # Handles the "chat.message" event when it's sent to us.
        self.send(text_data=event["text"])

# class NotificationConsumerSync(WebsocketConsumer):
#     user_dictionary = {}
#
#     def getList(self,dict):
#         list = []
#         for key in dict.keys():
#             list.append(key)
#
#         return list
#
#     def connect(self):
#         self.room_name = 'users'
#         # self.user = self.scope["user"]
#         # print(self.user.id)
#         # print(self.channel_name)
#         # print(self.room_name)
#         # print(self.scope['url_route'])
#         # print(self.scope['url_route']['kwargs'])
#         self.user_name = self.scope['url_route']['kwargs']['room_name']
#         print(self.user_name)
#         self.user_dictionary[self.user_name] = self.channel_name
#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_name,
#             self.channel_name
#         )
#
#         print(self.getList(self.user_dictionary))
#         users_list = self.getList(self.user_dictionary)
#         # await self.channel_layer.group_send(
#         #     self.room_name,
#         #     {
#         #         'type': 'users_list',
#         #         'users': json.dumps({'users':users_list,'action':'users_list'}),
#         #     },
#         # )
#         async_to_sync(self.channel_layer.group_send(
#                 self.room_name,
#                 {
#                     'type': 'users_list',
#                     'users': json.dumps({'users':users_list,'action':'users_list'}),
#                 },
#             ))
#         self.accept()
#         # print(self.channel_layer.__dict__)
#         # await self.channel_layer.group_send(
#         #     self.room_group_name,
#         #     {
#         #         'type': 'users_list',
#         #         'message': "allusers"
#         #     }
#         # )
#
#     def receive(self, text_data):
#         print(self.channel_name)
#         print(self.channel_layer)
#         print(self.user_name)
#         # print(text_data)
#         # channel_name = self.user_dictionary[]
#         # await self.channel_layer.group_add(
#         #     self.room_name,
#         #     self.channel_name,
#         #     # self.user_name
#         # )
#         send_data = json.loads(text_data)
#         print(send_data)
#         if(send_data.action == 'solo'):
#             reciever = self.user_dictionary[send_data.reciever]
#             print(reciever)
#             # await reciever.send(
#             #     self.room_name,
#             #     {
#             #         'type': 'notification_to_user',
#             #         'message': text_data,
#             #     },
#             # )
#             async_to_sync(self.channel_layer.group_send(
#                 self.room_name,
#                 {
#                     'type': 'notification_to_user',
#                     'message': text_data,
#                 },
#             ))
#         else:
#             async_to_sync(self.channel_layer.group_send(
#                 self.room_name,
#                 {
#                     'type': 'notification_broadcast',
#                     'message': text_data,
#                 },
#             ))
#
#     def users_list(self,event):
#         print(self.channel_layer)
#         self.send(text_data=event["users"])
#         # await self.send(
#         #     {
#         #         "users": self.user_dictionary
#         #     },
#         # )
#     def notification_to_user(self,event):
#         self.send(text_data=event["message"])
#
#
#     def notification_broadcast(self,event):
#         self.send(text_data=event["message"])
#
#     def disconnect(self, close_code):
#          # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_name,
#             self.channel_name
#         )
#         del self.user_dictionary[self.user_name]
#         print(self.user_dictionary)
#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_name,
#             {
#                 'type': 'users_list',
#                 'users': json.dumps({'users':"users_list",'action':'users_list'}),
#             }
#         )
        # await self.channel_layer.group_send(
        #     self.room_name,
        #     {
        #         'type': 'users_list',
        #         'users': json.dumps({'users':users_list,'action':'users_list'}),
        #     },
        # )
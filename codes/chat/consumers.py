import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from asgiref.sync import async_to_sync, sync_to_async
from chat.models import *
from .serializers import *
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from django.contrib.auth import get_user_model
from urllib.parse import urlparse, parse_qs
User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):

    user_dictionary = {}
    user_channels_details = {}
    user_counter = 0
    user_name = 'Anonymous'
    user_list = []
    user_channel_name_list = {} #dict of all active users
    user_keys_list = [] #dict of all active users
    access_token = 0
    room_name = ""
    room_exists =False

    
    @database_sync_to_async
    def get_room(self,user_id,room_name):
        # room_name = Channel.objects.get(name=room_name)
        # our_channel = ChannelMember.objects.filter(Channel=room_name).filter(user=user_id)
        try:
            # our_user = User.objects.get(id=user_id)
            room_name = Channel.objects.get(name=room_name)
            our_channel = ChannelMember.objects.filter(Channel=room_name).filter(user=user_id)
            return our_channel.exists()
        except :
            return False

    @database_sync_to_async
    def get_user_only(self,user_id):
        # our_channel = ChannelMember.objects.filter(Channel=room_name).filter(user=user_id)
        try:
            our_user = User.objects.filter(id=user_id)
            
            return our_user.exists()
        except User.DoesNotExist:
            return False

    # @database_sync_to_async
    # def get_username(self,userid):
    #         user_name = User.objects.get(id=userid)
    #         return user_name.username

    @database_sync_to_async
    def get_last_message(self, user_id):
        message = Message.objects.filter(user_id=user_id).last()
        return message.message

    @database_sync_to_async
    def get_channel_info(self,room_name):
        try:
            channel_info = Channel.objects.filter(name=room_name).first()
            if channel_info:
                channel_member = ChannelMember.objects.filter(Channel=channel_info).filter(user=self.user_id).first()
            else:
                return False
            return channel_member
        except Channel.DoesNotExist:
            return False
 
    async def connect(self):       
        try:
            parsed_query_string = parse_qs(self.scope["query_string"])
            if parsed_query_string:
                token = parsed_query_string.get(b"token")[0].decode("utf-8")
                self.access_token = AccessToken(token)
                self.user_id = self.access_token["user_id"]
                if self.user_id:
                    #Adding user in dict
                    self.user_channel_name_list[self.access_token["user_id"]] = self.channel_name
                    #Identifying user is in group or not
                    # self.scope["user"] = await self.get_user_only(self.user_id)
                    # self.scope["user"] = False
                    self.room_name =  parsed_query_string.get(b"roomname")[0].decode("utf-8")
                    self.room_exists = await self.get_room(self.user_id,self.room_name)
                    # if room_name != "no":
                    #     self.scope["user"] = await self.get_user(self.access_token["user_id"],
                    #             room_name)
                else:  

                    pass
            else:
                
                pass
        except TokenError as e:
            # Socket has not been accepted, so cannot send over it
            # print(self.unidentified_user)
            # await self.channel_layer.send(
            #             self.unidentified_user,
            #     {
            #         'type': 'error_message',
            #         'message': json.dumps({"message":f"{e}"})
            #     },
            #     )
            self.close()

        if self.room_exists:
            # self.user_id = self.access_token["user_id"]      
            # self.room_name = self.scope['url_route']['kwargs']['room_name']
            # self.room_group_name = 'chat_%s' % self.room_name
            self.channel_member = await self.get_channel_info(self.room_name)      
            await self.store_user_name(self.channel_name)
            if not self.channel_member:
                return 'No Channel defined'

            await self.accept()            
            await self.channel_layer.group_add(f"{self.room_name}", self.channel_name)

        

        else:
            self.close()

    async def receive(self, text_data):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        await self.load_message(text_data)
        send_data = json.loads(text_data)
        send_data = json.loads(text_data)
        # self.user_id = int(self.access_token["user_id"])
        send_data["User"] = str(self.user_id)
        
        await self.print_details(send_data)

        # if(send_data['action'] == 'store_user_name'):
        #     del self.user_dictionary[self.channel_name]
        #     self.user_dictionary[self.channel_name] = send_data['user_name']
        #     self.user_list.clear()
        #     self.user_list.extend(self.user_dictionary.values())
        #     self.user_channels_details[send_data['user_name']
        #                                ] = self.channel_name
        #     await self.channel_layer.group_send(
        #         self.room_group_name,
        #         {
        #             'type': 'users_list',
        #             'users': json.dumps({'users': self.user_list, 'action': 'users_list'}),
        #         },
        #         )
        # elif(send_data['action'] == 'solo'):
        #     # receiver = self.user_channels_details[send_data['receiver']]
        #     # receiver = int(self.scope['url_route']['kwargs']['receiver_id'])
        #     print("self.user_id(sender) >>>>>>>>",self.user_id )

        #     print("self.user_channel_name_list(receiver)>>>>", self.receiver_id)
        #     # del send_data['receiver']
        #     # send_data['sender'] = self
        #     # message = send_data['message']
        #     if self.user_channel_name_list.get(self.receiver_id):
        #         await self.channel_layer.send(
        #                 self.user_channel_name_list.get(self.receiver_id),
        #         {
        #             'type': 'notification_to_user',
        #             'message': json.dumps(send_data),
        #         },
        #         )
        #     else:
        #         await self.channel_layer.send(
        #                 self.user_channel_name_list.get(self.user_id ),
        #         {
        #             'type': 'error_message',
        #             'message': json.dumps({"message":"User is not currently active"})
        #         },
        #         )

                

        await self.channel_layer.group_send(
        self.room_name,
        {
            'type': 'notification_broadcast',
            'message':  json.dumps(send_data),
        },
        )
        # else:
        #     await self.channel_layer.send(
        #             self.user_channel_name_list.get(self.user_id ),
        #     {
        #         'type': 'error_message',
        #         'message': json.dumps({"message":"Invalid cred"})
        #     },
        #     )


    @sync_to_async
    def load_message(self, text_data):
        try:
            channel_info = Channel.objects.filter(name=self.room_name).first()
            message_details = {}
            # message_details['user'] = self.scope["user"].id
            message_details['media_link'] = json.loads(text_data)["media_link"]
            message_details['message_text'] = json.loads(text_data)["message_text"]
            message_details['meta_attributes'] = json.loads(text_data)["meta_attributes"]
            message_details['user'] = self.user_id
            message_details['channel'] = channel_info.id
            message_serializer = MessageChannelSerializers(data=message_details)
            message_serializer.is_valid(raise_exception=True)
            message = message_serializer.save()
            return MessageSerializers(message).data
        except Channel.DoesNotExist:
            return False



    async def send_info_to_user_group(self, event):
        message = event["text"]
        await self.send(text_data=json.dumps(message))

    async def send_last_message(self, event):
        last_msg = await self.get_last_message(self.user_id)
        last_msg["status"] = event["text"]
        await self.send(text_data=json.dumps(last_msg))




    async def store_user_name(self, channel):
        self.user_counter += 1
        # self.user_list.append(self.user_name+str(self.user_counter))
        self.user_dictionary[channel] = self.user_name
        self.user_list.clear()
        self.user_list.extend(self.user_dictionary.values())

    async def users_list(self, event):
        await self.send(text_data=event["users"])

    async def print_details(self, send_data):
        pass

   

    async def notification_broadcast(self, event):       
        await self.send(text_data=json.dumps( event["message"]))

    async def error_message(self, event):       
        await self.send(text_data=json.dumps( event["message"]))
    
    
    # Receive message from room group

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def disconnect(self, close_code):
        # Leave room group
        try:
            await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
            )
            del self.user_dictionary[self.channel_name]
            self.user_list.clear()
            self.user_list.extend(self.user_dictionary.values())
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'users_list',
                    'users': json.dumps({'users': self.user_list, 'action': 'users_list'}),
                },
            )
        except:
            self.close()

#=============================================================================================================

class MessageUserConsumer(AsyncWebsocketConsumer):

    user_dictionary = {}
    user_channels_details = {}
    user_counter = 0
    user_name = 'Anonymous'
    user_list = []
    user_channel_name_list = {} #dict of all active users
    user_keys_list = [] #dict of all active users
    access_token = 0
    receiver_id = 0
    receiver_id_exists = False
    
 

    @database_sync_to_async
    def get_user_only(self,user_id):
        # our_channel = ChannelMember.objects.filter(Channel=room_name).filter(user=user_id)
        try:
            our_user = User.objects.filter(id=user_id)
            
            return our_user.exists()
        except User.DoesNotExist:
            return False

    # @database_sync_to_async
    # def get_username(self,userid):
    #         user_name = User.objects.get(id=userid)
    #         return user_name.username



 
    async def connect(self):       
        try:
            parsed_query_string = parse_qs(self.scope["query_string"])
            if parsed_query_string:
                token = parsed_query_string.get(b"token")[0].decode("utf-8")
                self.access_token = AccessToken(token)
                self.user_id = self.access_token["user_id"]
                if self.user_id:
                    #Adding user in dict
                    self.user_channel_name_list[self.access_token["user_id"]] = self.channel_name
                    #Identifying user is in group or not
                    self.receiver_id = int(parsed_query_string.get(b"receiver_id")[0].decode("utf-8"))
                    self.receiver_id_exists = await self.get_user_only(self.receiver_id)
                   
                else:  

                    pass
            else:
                
                pass
        except TokenError as e:
            # Socket has not been accepted, so cannot send over it
            # print(self.unidentified_user)
            # await self.channel_layer.send(
            #             self.unidentified_user,
            #     {
            #         'type': 'error_message',
            #         'message': json.dumps({"message":f"{e}"})
            #     },
            #     )
            self.close()

    

        if self.receiver_id_exists:
            # self.user_id = self.access_token["user_id"]
            
            await self.accept() 
            self.user_keys_list = [i for i in self.user_channel_name_list.keys()]
            await self.send(text_data =json.dumps(
                {
                    'action': 'users_list',
                    'users':self.user_keys_list,
                },
            ))

        else:
            self.close()

    async def receive(self, text_data):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        send_data = json.loads(text_data)
        send_data = json.loads(text_data)
        # self.user_id = int(self.access_token["user_id"])
        send_data["User"] = str(self.user_id)

        # if(send_data['action'] == 'store_user_name'):
        #     del self.user_dictionary[self.channel_name]
        #     self.user_dictionary[self.channel_name] = send_data['user_name']
        #     self.user_list.clear()
        #     self.user_list.extend(self.user_dictionary.values())
        #     self.user_channels_details[send_data['user_name']
        #                                ] = self.channel_name
        #     await self.channel_layer.group_send(
        #         self.room_group_name,
        #         {
        #             'type': 'users_list',
        #             'users': json.dumps({'users': self.user_list, 'action': 'users_list'}),
        #         },
        #         )
            # receiver = self.user_channels_details[send_data['receiver']]
            # receiver = int(self.scope['url_route']['kwargs']['receiver_id'])
        # del send_data['receiver']
        # send_data['sender'] = self
        # message = send_data['message']
        if self.user_channel_name_list.get(self.receiver_id):
            await self.channel_layer.send(
                    self.user_channel_name_list.get(self.receiver_id),
            {
                'type': 'notification_to_user',
                'message': json.dumps(send_data),
            },
            )
        else:
            await self.channel_layer.send(
                    self.user_channel_name_list.get(self.user_id ),
            {
                'type': 'error_message',
                'message': json.dumps({"message":"User is not currently active"})
            },
            )

                



    @sync_to_async
    def load_message(self, text_data):
        try:
            channel_info = Channel.objects.filter(name=self.room_name).first()
            message_details = {}
            # message_details['user'] = self.scope["user"].id
            message_details['user'] = self.user_id
            message_details['meta_attributes'] = json.loads(text_data)["message"]
            message_details['channel'] = channel_info.id
            message_serializer = MessageSerializers(data=message_details)
            message_serializer.is_valid(raise_exception=True)
            message = message_serializer.save()
            return MessageSerializers(message).data
        except Channel.DoesNotExist:
            return False






    async def store_user_name(self, channel):
        self.user_counter += 1
        # self.user_list.append(self.user_name+str(self.user_counter))
        self.user_dictionary[channel] = self.user_name
        self.user_list.clear()
        self.user_list.extend(self.user_dictionary.values())

    async def users_list(self, event):
        await self.send(text_data=event["users"])

    async def print_details(self, send_data):
        pass

    async def notification_to_user(self, event):
        await self.send(text_data=event["message"])

    async def error_message(self, event):       
        await self.send(text_data=json.dumps( event["message"]))
    
    
    # Receive message from room group

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def disconnect(self, close_code):
        # Leave room group
        try:
            pass
            # await self.channel_layer.group_discard(
            # self.room_group_name,
            # self.channel_name
            # )
            # del self.user_dictionary[self.channel_name]
            # self.user_list.clear()
            # self.user_list.extend(self.user_dictionary.values())
            # await self.channel_layer.send(
            #     self.channel_name,
            #     {
            #         'type': 'users_list',
            #         'users': json.dumps({'users': self.user_list, 'action': 'users_list'}),
            #     },
            # )
        except:
            self.close()






#=======================================Queue============================================================


import redis

redisconn = redis.StrictRedis(
    host='127.0.0.1', port=6379, db=0, decode_responses=True)


class ChatConsumerQueue(AsyncWebsocketConsumer):
    pass
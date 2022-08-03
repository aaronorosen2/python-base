import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from asgiref.sync import async_to_sync, sync_to_async
from chat.models import Message,Channel, ChannelMember,Member,Org
from .serializers import OrgSerializers, MessageSerializers,ChannelSerializers, MemberSerializers, ChannelMemberSerializers
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    groups = ["general"]

    user_dictionary = {}
    user_channels_details = {}
    user_counter = 0
    user_name = 'Anonymous'
    user_list = []
    

    @database_sync_to_async
    def get_user(self,user_id,room_name):
        room_name = Channel.objects.get(name=room_name)
        our_channel = ChannelMember.objects.filter(Channel=room_name).filter(user=user_id)
        try:
            # our_user = User.objects.get(id=user_id)
            room_name = Channel.objects.get(name=room_name)
            our_channel = ChannelMember.objects.filter(Channel=room_name).filter(user=user_id)
            return our_channel.exists()
        except User.DoesNotExist:
            return False



    @database_sync_to_async
    def get_channel_info(self):
        try:
            channel_info = Channel.objects.filter(name=self.room_name).first()
            if channel_info:
                channel_member = ChannelMember.objects.filter(Channel=channel_info).filter(user=self.user_id).first()
            else:
                return False
            return channel_member
        except Channel.DoesNotExist:
            return False


    #   Connection Method  
    async def connect(self):
        parsed_query_string = parse_qs(self.scope["query_string"])
        token = parsed_query_string.get(b"token")[0].decode("utf-8")
        access_token = AccessToken(token)
        x =  await self.get_user(access_token["user_id"],self.scope['url_route']['kwargs']['room_name'])
       
        try:
            access_token = AccessToken(token)

            if access_token["user_id"] == int(self.scope['url_route']['kwargs']['user_id']):
                self.scope["user"] = await self.get_user(access_token["user_id"],self.scope['url_route']['kwargs']['room_name'])
            else:
                self.scope["user"] = False
        except TokenError as e:
            self.scope["user"] = False


        if self.scope["user"]:
            self.user_id = self.scope['url_route']['kwargs']['user_id']
        
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'chat_%s' % self.room_name
            self.channel_member = await self.get_channel_info()
            
            await self.store_user_name(self.channel_name)

            if not self.channel_member:
                return 'No Channel defined'

            await self.accept()            
            await self.channel_layer.group_add(f"{self.room_name}", self.channel_name)
        else:
            self.close()
    # Receive message from WebSocket

    async def receive(self, text_data):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        send_data = json.loads(text_data)
        send_data = json.loads(text_data)
        await self.print_details(send_data)

        if(send_data['action'] == 'store_user_name'):
            del self.user_dictionary[self.channel_name]
            self.user_dictionary[self.channel_name] = send_data['user_name']
            self.user_list.clear()
            self.user_list.extend(self.user_dictionary.values())
            self.user_channels_details[send_data['user_name']
                                       ] = self.channel_name
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'users_list',
                    'users': json.dumps({'users': self.user_list, 'action': 'users_list'}),
                },
            )
        elif(send_data['action'] == 'solo'):
            reciever = self.user_channels_details[send_data['reciever']]
            del send_data['reciever']
            # send_data['sender'] = self
            # message = send_data['message']
            await self.channel_layer.send(
                    reciever    ,
                {
                    'type': 'notification_to_user',
                    'message': json.dumps(send_data),
                },
            )
        elif(send_data['action'] == 'broadcast'):
            await self.load_message(text_data)

            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'notification_broadcast',
                    'message': send_data['message'],
                },
            )

    @sync_to_async
    def load_message(self, text_data):
        try:
            channel_info = Channel.objects.filter(name=self.room_name).first()
            message_details = {}
            # message_details['user'] = self.scope["user"].id
            message_details['user'] = self.user_id
            message_details['meta_attributes'] = text_data
            message_details['channel'] = channel_info.id
            message_serializer = MessageSerializers(data=message_details)
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



    @database_sync_to_async
    def get_last_message(self, user_id):
        message = Message.objects.filter(user_id=user_id).last()
        return message.message

    async def store_user_name(self, channel):
        self.user_counter += 1
        # self.user_list.append(self.user_name+str(self.user_counter))
        self.user_dictionary[channel] = self.user_name
        self.user_list.clear()
        self.user_list.extend(self.user_dictionary.values())

    async def users_list(self, event):
        # print(self.channel_layer)
        await self.send(text_data=event["users"])

    async def print_details(self, send_data):
        pass

    async def notification_to_user(self, event):
        await self.send(text_data=event["message"])

    async def notification_broadcast(self, event):       
        message = event["text"]
        await self.send(text_data=json.dumps(message))
    
    
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

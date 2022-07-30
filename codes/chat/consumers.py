import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

from asgiref.sync import async_to_sync, sync_to_async

from chat.models import Message

from .models import Channel, ChannelMember

from .serializers import OrgSerializers, MessageSerializers,ChannelSerializers

class ChatConsumer(AsyncWebsocketConsumer):
    groups = ["general"]

    user_dictionary = {}
    user_channels_details = {}
    user_counter = 0
    user_name = 'Anonymous'
    user_list = []

    @database_sync_to_async
    def get_channel_info(self):
        try:
            channel_info = Channel.objects.filter(name=self.room_name).first()
            print(" ***** channel_info ********", channel_info)
            if channel_info:
                channel_member = ChannelMember.objects.filter(Channel=channel_info).filter(user=self.user_id).first()
                print("******** channel_member *******", channel_member)
            else:
                return False
            return channel_member
        except Channel.DoesNotExist:
            print("ERROR: CHANNEL doesnt exit ********")
            return False

    async def connect(self):
        print(self.scope)
        # if self.scope["user"] is not AnonymousUser:
        if self.scope['url_route']['kwargs']['user_id'] and self.scope['url_route']['kwargs']['room_name']:
            # self.user_id = self.scope["user"].id
            self.user_id = self.scope['url_route']['kwargs']['user_id']
        
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'chat_%s' % self.room_name
            self.channel_member = await self.get_channel_info()
            
            await self.store_user_name(self.channel_name)

            if not self.channel_member:
                return 'No Channel defined'

            await self.accept()            
            await self.channel_layer.group_add(f"{self.room_name}", self.channel_name)

    # Receive message from WebSocket

    async def receive(self, text_data):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user_id = self.scope['url_route']['kwargs']['user_id']

        send_data = json.loads(text_data)
        print('test_data =============', send_data, self.channel_name)
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
            # print(reciever)
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
            print(self.room_name)
            channel_info = Channel.objects.filter(name=self.room_name).first()
            print(channel_info)
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
            print('Channel.DoesNotExist *******************')
            return False


    async def disconnect(self, close_code):
        print('disconnect')
        # Leave room group
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

    async def send_info_to_user_group(self, event):
        message = event["text"]
        await self.send(text_data=json.dumps(message))

    async def send_last_message(self, event):
        last_msg = await self.get_last_message(self.user_id)
        last_msg["status"] = event["text"]
        await self.send(text_data=json.dumps(last_msg))



    @database_sync_to_async
    def get_last_message(self, user_id):
        print('user_id==========',user_id)
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
        print(self.user_name)
        print(self.user_dictionary)
        print(self.user_list)
        print(send_data)

    async def notification_to_user(self, event):
        await self.send(text_data=event["message"])

    async def notification_broadcast(self, event):
        await self.send(text_data=event["message"])
    # Receive message from room group

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


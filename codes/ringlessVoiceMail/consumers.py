import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from asgiref.sync import sync_to_async
# from .admin import ClientsAdmin
from .models import RinglessClients, RinglessVoiceMail
from .serializers import RinglessSerializers, RinglessVoiceMailSerializer
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
from django.db import models

User = get_user_model()

class RinglessVoiceMailConsumer(AsyncWebsocketConsumer):

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
        try:
            our_user = User.objects.filter(id=user_id)
            return our_user.exists()
        except User.DoesNotExist:
            return False

    @database_sync_to_async
    def clients_add(self,channel,user_id):
            createChannel = {'channel_name':channel,
            'modified_at' : models.DateTimeField(auto_now=True)
            }
            RinglessClients.objects.update_or_create(user_id = user_id, defaults=createChannel)
            return True

 
    async def connect(self):       
        try:
            parsed_query_string = parse_qs(self.scope["query_string"])
            if parsed_query_string:
                token = parsed_query_string.get(b"token")[0].decode("utf-8")
                self.access_token = AccessToken(token)
                self.user_id = int(self.access_token["user_id"])
                if self.user_id:
                    #Identifying receiver exist
                    self.user_channel_name_list[self.access_token["user_id"]] = str(self.channel_name)
                    await self.clients_add(self.channel_name,self.user_id)
                    self.receiver_id = int(parsed_query_string.get(b"receiver_id")[0].decode("utf-8"))
                    self.receiver_id_exists = await self.get_user_only(self.receiver_id)
                else:  

                    pass
            else:
                
                pass
        except TokenError as e:
            self.close()

    

        if self.receiver_id_exists:
            await self.accept() 
            self.user_keys_list = [i for i in self.user_channel_name_list.keys()]
            await self.send(text_data =json.dumps(
                {
                    'action': 'users_list',
                    'users': self.user_keys_list,
                    'success':'true'
                },
            ))

        else:
            self.close()

    async def receive(self, text_data):
        await self.load_message(text_data)

        send_data = json.loads(text_data)
        send_data["User"] = str(self.user_id)

        
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
            load_audio = {}
            load_audio['id'] = str(self.receiver_id)
            load_audio['user'] = str(self.user_id)
            load_audio['created_at'] = json.loads(text_data)["created_at"]
            load_audio["voiceMail_name"] = json.loads(text_data)["voiceMail_name"]
            # audio_serializer = RinglessSerializers(data=load_audio)
            
            audio_serializer = RinglessVoiceMailSerializer(data=load_audio)
            audio_serializer.is_valid()
            audio = audio_serializer.save()
            return RinglessVoiceMailSerializer(audio).data
        except Exception as e:
            return False

    async def store_user_name(self, channel):
        self.user_counter += 1
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

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def disconnect(self, close_code):
        self.close()
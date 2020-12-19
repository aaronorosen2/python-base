# from channels.generic.websocket import AsyncWebsocketConsumer
# import json
# from channels.generic.websocket import WebsocketConsumer
# from asgiref.sync import async_to_sync


import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):

    user_dictionary = {}
    user_channels_details = {}
    user_counter = 0
    user_name = 'Anonymous'
    user_list = []

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # store user details
        await self.store_user_name(self.channel_name)
        # sends the user list
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'users_list',
                'users': json.dumps({'users': self.user_list, 'action': 'users_list'}),
            },
        )
        await self.accept()


    # Receive message from WebSocket
    async def receive(self, text_data):

        send_data = json.loads(text_data)        
        if(send_data['action'] == 'store_user_name'):
            
            del self.user_dictionary[self.channel_name]
            self.user_dictionary[self.channel_name] = send_data['user_name']
            self.user_list.clear()
            self.user_list.extend(self.user_dictionary.values())
            self.user_channels_details[send_data['user_name']] = self.channel_name
            # await self.print_details(send_data)
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
                reciever,
                {
                    'type': 'notification_to_user',
                    'message': json.dumps(send_data),
                },
            )
        elif(send_data['action'] == 'broadcast'):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'notification_broadcast',
                    'message': text_data,
                },
            )
    
    async def disconnect(self, close_code):
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

    async def store_user_name(self, channel):
        self.user_counter += 1
        # self.user_list.append(self.user_name+str(self.user_counter))
        self.user_dictionary[channel] = self.user_name
        self.user_list.clear()
        self.user_list.extend(self.user_dictionary.values())

    async def users_list(self,event):
        # print(self.channel_layer)
        await self.send(text_data=event["users"])


    async def print_details(self,send_data):
        print(self.user_name)
        print(self.user_dictionary)
        print(self.user_list)
        print(send_data)

    async def notification_to_user(self,event):
        await self.send(text_data=event["message"])


    async def notification_broadcast(self,event):
        await self.send(text_data=event["message"])
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

from queue import Queue
import redis
redisconn = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)
import time

class NotificationConsumerQueue(AsyncWebsocketConsumer):

    user_dictionary = {}
    user_channels_details = {}
    user_counter = 0
    user_name = 'Anonymous'
    user_list = []
    

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.channel_layer.group_add(
            'all_users',
            self.channel_name
        )
        # enter in back queue
        # redisconn.set('room_name',self.room_group_name)
        # redisconn.lpush('roomlist', self.room_group_name)
        redisconn.sadd('room_names', self.room_group_name)
        # redisconn.hset('back',
        #                self.channel_name,
        #                self.room_group_name)
        # store user details
        # redisconn.hset('back',
        #                self.channel_name,
        #                self.user_name)
        await self.store_user_name(self.channel_name)
        # sends the user list
        listOfLiveUsers = redisconn.hvals(self.channel_name+'@live')
        # print(listOfLiveUsers)
        listOfBackUsers = redisconn.hvals(self.channel_name+'@back')
        if(self.room_group_name != 'chat_admin'):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'users_list',
                    'users': json.dumps(
                        {'live_users': listOfLiveUsers,
                            'action': 'users_list',
                            'back_users':listOfBackUsers
                        }),
                },
            )
        await self.accept()


    # Receive message from WebSocket
    async def receive(self, text_data):

        send_data = json.loads(text_data)
        if(send_data['action'] == 'store_user_name'):
            
            del self.user_dictionary[self.channel_name]
            self.user_dictionary[self.channel_name] = send_data['user_name']
            self.user_list.clear()
            self.user_list.extend(self.user_dictionary.values())
            self.user_channels_details[send_data['user_name']] = self.channel_name
            # await self.print_details(send_data)
            redisconn.hset(self.room_group_name+'@back',
                       self.channel_name,
                       send_data['user_name'])
            listOfLiveUsers = redisconn.hvals(self.room_group_name+'@live')
            listOfBackUsers = redisconn.hvals(self.room_group_name+'@back')
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'users_list',
                    'users': json.dumps(
                        # {'users': listOfLiveUsers, 'action': 'users_list'}
                        {'live_users': listOfLiveUsers,
                        'action': 'users_list',
                        'back_users':listOfBackUsers
                        }),
                },
            )
        elif(send_data['action'] == 'solo'):
            reciever = self.user_channels_details[send_data['reciever']]
            # print(reciever)
            del send_data['reciever']
            # send_data['sender'] = self
            # message = send_data['message']
            await self.channel_layer.send(
                reciever,
                {
                    'type': 'notification_to_user',
                    'message': json.dumps(send_data),
                },
            )
        elif(send_data['action'] == 'broadcast'):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'notification_broadcast',
                    'message': text_data,
                },
            )
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        del self.user_dictionary[self.channel_name]
        self.user_list.clear()
        self.user_list.extend(self.user_dictionary.values())
        if(redisconn.hexists(self.room_group_name+'@live',self.channel_name)):
            redisconn.hdel(self.room_group_name+'@live', self.channel_name)
        else:
            redisconn.hdel(self.room_group_name+'@back', self.channel_name)
        listOfLiveUsers = redisconn.hvals(self.room_group_name+'@live')
        listOfBackUsers = redisconn.hvals(self.room_group_name+'@back')
        dataListOfUsers = {'type': 'users_list',
                        'users': json.dumps(
                            {'live_users': listOfLiveUsers,
                            'action': 'users_list',
                            'back_users':listOfBackUsers}
                        ),}
        await self.channel_layer.group_send(
            self.room_group_name,
            dataListOfUsers,
        )

    async def store_user_name(self, channel):
        self.user_counter += 1
        # self.user_list.append(self.user_name+str(self.user_counter))
        self.user_dictionary[channel] = self.user_name
        self.user_list.clear()
        self.user_list.extend(self.user_dictionary.values())
        # redisconn.zadd("backstage", {channel:time.time()+60})

    async def users_list(self,event):
        # print(self.channel_layer)
        await self.send(text_data=event["users"])


    async def print_details(self,send_data):
        print(self.user_name)
        print(self.user_dictionary)
        print(self.user_list)
        print(send_data)

    async def notification_to_user(self,event):
        await self.send(text_data=event["message"])
    
    async def notification_to_queue_member(self,event):
        await self.send(text_data=json.dumps(event["message"]))


    async def notification_broadcast(self,event):
        await self.send(text_data=event["message"])
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
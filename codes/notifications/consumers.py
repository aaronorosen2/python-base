# from channels.generic.websocket import AsyncWebsocketConsumer
# import json
# from channels.generic.websocket import WebsocketConsumer
# from asgiref.sync import async_to_sync


from asgiref.sync import async_to_sync, sync_to_async
from queue import Queue
from vconf.models import RoomInfo, RoomVisitors
from s3_uploader.serializers import RoomInfoSerializer, RoomVisitorsSerializer
import time
import redis
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
            self.user_channels_details[send_data['user_name']
                                       ] = self.channel_name
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


redisconn = redis.StrictRedis(
    host='redis', port=6379, db=0, decode_responses=True)


class NotificationConsumerQueue(AsyncWebsocketConsumer):

    user_dictionary = {}
    user_channels_details = {}
    user_counter = 0
    user_name = 'Anonymous'
    user_list = []
    room_representative = {}

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
        room_info = await self.get_room_info(self.room_name)
        if(room_info != False):
            room_info_dict = {'logo_url': room_info.logo_url,
                              'room_name': room_info.room_name,
                              'action': 'room_logo'}
            # print(room_info_dict)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'notification_broadcast',
                    'message': json.dumps(room_info_dict),
                },
            )
        else:
            room_info_dict = {'logo_url': "",
                              'room_name': "Please Upload Room Info!",
                              'action': 'room_logo'}
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'notification_broadcast',
                    'message': json.dumps(room_info_dict),
                },
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
        listOfLiveUsers = redisconn.hvals(self.room_group_name+'@live')
        # print(listOfLiveUsers)
        listOfBackUsers = redisconn.hvals(self.room_group_name+'@back')
        if(self.room_group_name != 'chat_admin'):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'users_list',
                    'users': json.dumps(
                        {'live_users': listOfLiveUsers,
                            'action': 'users_list',
                            'back_users': listOfBackUsers
                         }),
                },
            )
        await self.accept()

    # Receive message from WebSocket

    async def receive(self, text_data):

        send_data = json.loads(text_data)
        # print(send_data)
        if(send_data['action'] == 'store_user_name'):

            del self.user_dictionary[self.channel_name]
            self.user_dictionary[self.channel_name] = send_data['user_name']
            self.user_list.clear()
            self.user_list.extend(self.user_dictionary.values())
            self.user_channels_details[send_data['user_name']] = self.channel_name
            if(send_data['roomVisitor']):
                if(redisconn.hexists("roomrepresentative", self.room_group_name)):
                    message = {
                        'action': 'queue_status',
                        'message': 'go_live'
                    }
                    data = {"type": "notification_to_queue_member",
                            "message": message}
                    await self.channel_layer.send(
                        self.channel_name,
                        data,
                    )
            else:
                await self.send_meeting_url_to_slack(send_data)
            # await self.print_details(send_data)
            redisconn.hset(self.room_group_name+'@back',
                           self.channel_name,
                           send_data['user_name'])
            listOfLiveUsers = redisconn.hvals(self.room_group_name+'@live')
            listOfBackUsers = redisconn.hvals(self.room_group_name+'@back')
            await self.insert_room_visitor(send_data)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'users_list',
                    'users': json.dumps(
                        # {'users': listOfLiveUsers, 'action': 'users_list'}
                        {'live_users': listOfLiveUsers,
                         'action': 'users_list',
                         'back_users': listOfBackUsers
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
        elif (send_data['action'] == 'join_room'):
            message = {
                'action': 'queue_status',
                'message': 'go_live'
            }
            # await sync_to_async(print(send_data))
            # print(send_data)
            if(send_data['representatve'] == True):
                # print("representative...")
                # await self.printData(send_data)
                redisconn.hset("roomrepresentative",
                               self.room_group_name,
                               self.channel_name)
            else:
                data = {"type": "notification_to_queue_member", "message": message}
                reciever = self.user_channels_details[send_data['client']]
                redisconn.hdel(self.room_group_name+'@back', reciever)
                await self.channel_layer.send(
                    reciever,
                    data,
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
        if(redisconn.hexists(self.room_group_name+'@live', self.channel_name)):
            redisconn.hdel(self.room_group_name+'@live', self.channel_name)
        else:
            redisconn.hdel(self.room_group_name+'@back', self.channel_name)
        redisconn.hdel("roomrepresentative", self.room_group_name)
        listOfLiveUsers = redisconn.hvals(self.room_group_name+'@live')
        listOfBackUsers = redisconn.hvals(self.room_group_name+'@back')
        dataListOfUsers = {'type': 'users_list',
                           'users': json.dumps(
                               {'live_users': listOfLiveUsers,
                                'action': 'users_list',
                                'back_users': listOfBackUsers}
                           ), }
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

    @sync_to_async
    def printData(self, dataDict):
        print(dataDict)

    @sync_to_async
    def send_meeting_url_to_slack(self, user_data):
        import requests
        import json
        url = 'https://hooks.slack.com/services/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'
        # send_message(text="Hi, I'm a test message.")
        slack_message = user_data['user_name'] + \
            " wants you to join the room " + user_data['meeting_url']
        body = {"text": "%s" % slack_message,
                'username': user_data['user_name']}
        requests.post(url, data=json.dumps(body))

    @sync_to_async
    def get_room_info(self, room_name):
        # print(RoomInfo.objects.get(room_name=room_name))
        try:
            room_info = RoomInfo.objects.get(room_name=room_name)
            return room_info
        except RoomInfo.DoesNotExist:
            return False
        # if(room_info):
        #     return room_info
        # return False

    @sync_to_async
    def insert_room_visitor(self, user_details):
        room_info = RoomInfo.objects.get(room_name=self.room_name)
        user_details['room'] = room_info.id
        # print(user_details)
        room_visitor_serializer = RoomVisitorsSerializer(data=user_details)
        room_visitor_serializer.is_valid(raise_exception=True)
        room_visitor = room_visitor_serializer.save()
        # print(room_visitor)
        return RoomVisitorsSerializer(room_visitor).data

    # async def get_room_info(self, room_name):
    #     room_info = sync_to_async(RoomInfo.objects.get(room_name=room_name))()
    #     await print(room_info)
    #     # room_info = room_info.__dict__
    #     # room_info['action'] = 'logo_url'
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type': 'notification_broadcast',
    #             'message': room_info,
    #         },
    #     )

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

    async def notification_to_queue_member(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    async def notification_broadcast(self, event):
        await self.send(text_data=event["message"])
    # Receive message from room group

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

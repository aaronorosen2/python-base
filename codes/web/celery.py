import os
from celery import Celery
import redis
from asgiref.sync import async_to_sync
import channels.layers
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

app = Celery('web')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

channel_layer = channels.layers.get_channel_layer()
redisconn = redis.StrictRedis(
    host='redis', port=6379, db=0, decode_responses=True)
# sudo docker build --no-cache -t python_sfapp_celery_worker -f celery.Dockerfile .


@app.task()
def send_wait_notification_customer():
    room_list = redisconn.smembers('room_names')
    room_list = list(room_list)
    room_list.remove('chat_admin')
    for room in room_list:
        listOfBackUsers = redisconn.hkeys(room+'@back')
        for user in listOfBackUsers:
            message = {
                'action': "queue_status",
                'message': "Please Wait For Representative!!"
            }
            notification = {
                'type': 'notification_broadcast',
                'message': json.dumps(message),
            }
            async_to_sync(channel_layer.send)(user, notification)


@app.task()
def room_details():
    room_list = redisconn.smembers('room_names')
    all_users = []
    room_list = list(room_list)
    room_list.remove('chat_admin')
    for room in room_list:
        listOfLiveUsers = redisconn.hvals(room+'@live')
        listOfBackUsers = redisconn.hvals(room+'@back')
        # if(len(listOfLiveUsers) > 0 or len(listOfBackUsers) > 0):
        users_dict = {'room_name': room,
                      'live_users': listOfLiveUsers, 'back_users': listOfBackUsers}
        all_users.append(users_dict)

    if(len(all_users) > 0):
        dataListOfUsers = {'type': 'users_list',
                           'users': json.dumps(
                               {'all_users': all_users,
                                'action': 'all_users'}
                           ), }
        async_to_sync(channel_layer.group_send)('chat_admin', dataListOfUsers)


@app.task()
def schedule_member():
    print("schedule member!")
    # print("room name",redisconn.get('room_name'))
    # room_name = redisconn.get('room_name')
    room_list = redisconn.smembers('room_names')
    all_users = []
    room_list = list(room_list)
    room_list.remove('chat_admin')
    for room in room_list:
        backstage = redisconn.hkeys(room+'@back')
        live = redisconn.hkeys(room+'@live')
        if(len(live) > 0):
            remove_live(room, live)
        if(len(backstage) > 0):
            send_live(room, backstage[0:2])

        listOfLiveUsers = redisconn.hvals(room+'@live')
        listOfBackUsers = redisconn.hvals(room+'@back')
        users_dict = {'room_name': room,
                      'live_users': listOfLiveUsers, 'back_users': listOfBackUsers}
        all_users.append(users_dict)
        details_room = {'type': 'users_list',
                        'users': json.dumps(
                            {'live_users': listOfLiveUsers,
                             'action': 'users_list',
                             'back_users': listOfBackUsers}
                        ), }
        async_to_sync(channel_layer.group_send)(room, details_room)

    # dataListOfUsers = {'type': 'users_list',
    #                 'users': json.dumps(
    #                     {'all_users': all_users,
    #                     'action': 'all_users'}
    #                 ),}
    # async_to_sync(channel_layer.group_send)('all_users', dataListOfUsers)

    # if (room_name == None):
    #     room_name = "sample"
    # backstage = redisconn.hkeys('back')
    # live = redisconn.hkeys('live')
    # if(len(live) > 0):
    #     remove_live(live)
    # if(len(backstage) > 0):
    #     send_live(backstage[0:2])

    # listOfLiveUsers = redisconn.hvals('live')
    # listOfBackUsers = redisconn.hvals('back')
    # dataListOfUsers = {'type': 'users_list',
    #                 'users': json.dumps(
    #                     {'live_users': listOfLiveUsers,
    #                     'action': 'users_list',
    #                     'back_users':listOfBackUsers}
    #                 ),}
    # async_to_sync(channel_layer.group_send)(room_name, dataListOfUsers)

    return


def remove_live(room_name, live_channels_name):
    for key in live_channels_name:
        redisconn.hdel(room_name+'@live', key)
        print("sending notification expired!!!!")
        message = {
            'action': 'queue_status',
            'message': 'expired'
        }
        data = {"type": "notification_to_queue_member", "message": message}
        async_to_sync(channel_layer.send)(key, data)

    # listOfLiveUsers = redisconn.hvals('live')
    # listOfBackUsers = redisconn.hvals('back')
    # dataListOfUsers = {'type': 'users_list',
    #                 'users': json.dumps(
    #                     {'live_users': listOfLiveUsers,
    #                     'action': 'users_list',
    #                     'back_users':listOfBackUsers}
    #                 ),}

    # async_to_sync(channel_layer.group_send)('chat_users', dataListOfUsers)


def send_live(room_name, back_channel_names):
    # print("send_live")
    # print(back_channel_names)
    backstage = redisconn.hmget(room_name+'@back', back_channel_names)
    # print(backstage)
    res = {back_channel_names[i]: backstage[i]
           for i in range(len(back_channel_names))}
    redisconn.hmset(room_name+'@live', res)
    for key in back_channel_names:
        redisconn.hdel(room_name+'@back', key)
        print("sending notification live!!!")
        message = {
            'action': 'queue_status',
            'message': 'go_live'
        }
        data = {"type": "notification_to_queue_member", "message": message}
        async_to_sync(channel_layer.send)(key, data)


@app.task()
def hello():
    print("Hello there!")


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.task()
def check_user_connectivity():
    import datetime
    room_list = list(redisconn.smembers('room_names'))
    connected_users = redisconn.hgetall("connected_users")
    seconds_in_day = 24 * 60 * 60
    for k, v in connected_users.items():
        difference_time = datetime.datetime.now() - datetime.datetime.strptime(v,
                                                                               '%Y-%m-%d %H:%M:%S.%f')

        print('/////')
        minutes, seconds = divmod(difference_time.days * seconds_in_day + difference_time.seconds,
                                  60)
        print(difference_time)
        print(minutes, seconds)
        print('/////')
        if minutes > 6:
            redisconn.hdel("connected_users", k)
            for i in room_list:
                if redisconn.hexists(i+'@live', k):
                    redisconn.hdel(i+'@live',
                                   k)
                    async_to_sync(channel_layer.group_discard)(
                        i, k)
                    return "Available In Live Users List"
                if redisconn.hexists(i+'@back', k):
                    redisconn.hdel(i+'@back',
                                   k)
                    async_to_sync(channel_layer.group_discard)(
                        i, k)
                    return "Available In Back Users List"
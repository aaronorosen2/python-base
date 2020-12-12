import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

app = Celery('web')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
import redis
from asgiref.sync import async_to_sync
import channels.layers
channel_layer = channels.layers.get_channel_layer()

redisconn = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)
# sudo docker build --no-cache -t python_sfapp_celery_worker -f celery.Dockerfile .
@app.task()
def schedule_member():
    #list_stage_members = redisconn.zrange('live', 0,3)
    #len_stage_members = len(list_stage_members)
    #[loop_live_task('live', 'backstage', i, list_stage_members) for i in range(len_stage_members)]
    #redisconn.zremrangebyrank('backstage', 0, len_stage_members-1)
    #[loop_pooled_task('backstage', 'pooled', i) for i in range(len_stage_members)]
    #redisconn.zremrangebyrank('pooled', 0, len_stage_members-1)
    print("schedule member!!!!")
    backstage = redisconn.hkeys('back')
    live = redisconn.hkeys('live')
    # backstage = redisconn.zrange("backstage", 0, 6, withscores=True)
    # live = redisconn.zrange("live", 0, -1, withscores=True)
    # live_count = redisconn.zcard("live")
    print('backstage', backstage)
    print('live', live)
    if(len(live) > 0):
        for key in live:
            redisconn.hdel('live', key)
            message = {
                'action': 'queue_status',
                'message': 'expired'
            }
            data = {"type": "notification_to_queue_member", "message": message}
            async_to_sync(channel_layer.send)(key, data)
    if(len(backstage) > 0):
        send_live(backstage[0:2])
        # [send_live(i) for i in backstage]
    # if live_count >= 6:
       #remove_live(live[0])
       # pass
    # if backstage:
    #    [send_live(i) for i in backstage]
    #   if live_count>1:
    #      redisconn.zremrangebyrank("live", 0,0)
    #
    #   print("live added", redisconn.zadd("live", {backstage[0]:time.time()}))
    return


#from dreampotential_api.users.consumers import get_data

def remove_live(email):
    print(email)


    # redisconn.zrem("live", email)
    # channel_name = redisconn.hget("channel:room", email)
    # if channel_name:
    #    # data = get_data()
    #    message_data = {"type":"notify_users", "text":"expired"}
    #    async_to_sync(channel_layer.group_send)('room', message_data)
    # return

def send_live(back_channel_names):
    print("send_live")
    print(back_channel_names)
    backstage = redisconn.hmget('back', back_channel_names)
    print(backstage)
    res = {back_channel_names[i]: backstage[i] for i in range(len(back_channel_names))}
    print(res)
    redisconn.hmset('live', res)
    for key in back_channel_names:
        redisconn.hdel('back', key)
        message = {
            'action': 'queue_status',
            'message': 'go_live'
        }
        data = {"type": "notification_to_queue_member", "message": message}
        async_to_sync(channel_layer.send)(key, data)
    print("sending message!!!")
    # response_list = redisconn.hmget('back', channel_names)
    # redisconn.hset()
    # channel_name = redisconn.hget("channel:room", email)
    # data = {"type":"notify_users", "text":{"message_type":"go_live", "email":email}}
    # if channel_name:
    #    print(channel_name)
    #    print(email)
    #    async_to_sync(channel_layer.send)(channel_name, data)
    # return

@app.task()
def hello():
    print("Hello there!")

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# import os

# from celery import Celery
# from celery.schedules import crontab

# # set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

# app = Celery('celeryProject')

# # Using a string here means the worker doesn't have to serialize
# # the configuration object to child processes.
# # - namespace='CELERY' means all celery-related configuration keys
# #   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.conf.broker_url = 'redis://localhost:6378/'

# app.conf.beat_schedule = {
#     'pop-user-every-30-seconds': {
#         'task': 'tasks.schedule_member',
#         'schedule': 30.0,
#         'args': (16, 16)
#     },
# }
# app.conf.timezone = 'UTC'

# # Load task modules from all registered Django app configs.
# app.autodiscover_tasks()

# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
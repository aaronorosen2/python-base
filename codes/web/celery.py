import os
from celery import Celery
import redis
from asgiref.sync import async_to_sync
import channels.layers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

app = Celery('web')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

channel_layer = channels.layers.get_channel_layer()
redisconn = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)
# sudo docker build --no-cache -t python_sfapp_celery_worker -f celery.Dockerfile .

@app.task()
def schedule_member():
    print("schedule member!!!!")
    backstage = redisconn.hkeys('back')
    live = redisconn.hkeys('live')
    if(len(live) > 0):
        remove_live(live)
    if(len(backstage) > 0):
        send_live(backstage[0:2])

    return


def remove_live(live_channels_name):
    for key in live_channels_name:
        redisconn.hdel('live', key)
        print("sending notification expired!!!")
        message = {
            'action': 'queue_status',
            'message': 'expired'
        }
        data = {"type": "notification_to_queue_member", "message": message}
        async_to_sync(channel_layer.send)(key, data)


def send_live(back_channel_names):
    # print("send_live")
    # print(back_channel_names)
    backstage = redisconn.hmget('back', back_channel_names)
    # print(backstage)
    res = {back_channel_names[i]: backstage[i] for i in range(len(back_channel_names))}
    # print(res)
    redisconn.hmset('live', res)
    for key in back_channel_names:
        redisconn.hdel('back', key)
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

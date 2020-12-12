from celery import shared_task
import time
import redis
from asgiref.sync import async_to_sync
import channels.layers
channel_layer = channels.layers.get_channel_layer()
redisconn = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)
# sudo docker build --no-cache -t python_sfapp_celery_worker -f celery.Dockerfile .
@shared_task
def schedule_member():
    #list_stage_members = redisconn.zrange('live', 0,3)
    #len_stage_members = len(list_stage_members)
    #[loop_live_task('live', 'backstage', i, list_stage_members) for i in range(len_stage_members)]
    #redisconn.zremrangebyrank('backstage', 0, len_stage_members-1)
    #[loop_pooled_task('backstage', 'pooled', i) for i in range(len_stage_members)]
    #redisconn.zremrangebyrank('pooled', 0, len_stage_members-1)
    print("schedule member!!!!")
    backstage = redisconn.zrange("backstage", 0, 6)
    live = redisconn.zrange("live", 0, -1)
    live_count = redisconn.zcard("live")
    if live_count >= 6:
       #remove_live(live[0])
       pass
    if backstage:
       [send_live(i) for i in backstage]
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

def send_live(email):
    print(email)
    # channel_name = redisconn.hget("channel:room", email)
    # data = {"type":"notify_users", "text":{"message_type":"go_live", "email":email}}
    # if channel_name:
    #    print(channel_name)
    #    print(email)
    #    async_to_sync(channel_layer.send)(channel_name, data)
    # return
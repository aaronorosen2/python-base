import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

app = Celery('web')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

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
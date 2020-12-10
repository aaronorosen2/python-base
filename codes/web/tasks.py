from celery import shared_task

# sudo docker build --no-cache -t python_sfapp_celery_worker -f celery.Dockerfile .
@shared_task
def hello():
    print("Hello there!")
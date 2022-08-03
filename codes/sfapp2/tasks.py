from celery import shared_task
from .utils.twilio import update_list_call


@shared_task()
def update_calls_to_database():
    update_list_call()

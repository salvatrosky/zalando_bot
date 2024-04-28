from __future__ import absolute_import, unicode_literals

from celery import shared_task
from core.celery import app
import time


@shared_task
def proccess_link(message, user_id):
    print("Start proccess_link with args:", message, user_id)
    time.sleep(10)
    return "Task with a runit 10-second delay completed"+str(time.time())

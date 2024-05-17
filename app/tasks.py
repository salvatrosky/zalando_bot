from __future__ import absolute_import, unicode_literals
from celery import shared_task
import asyncio
from app.zalando_scrapper import test_scraper
import logging
import redis
import time


logger = logging.getLogger(__name__)

redis_client = redis.StrictRedis(host='redis', port=6379, db=0)


@shared_task
def proccess_link(message, user_id):
    logger.info(f"Start proccess_link with args: {message}, {user_id}")
    result = asyncio.run(test_scraper(message, user_id))
    return result


@shared_task
def check_prices():
    from app.models import Product

    lock_name = "periodic_lock"
    lock = redis_client.lock(lock_name, timeout=60*5)

    if lock.acquire(blocking=False):
        try:
            products = Product.objects.all()

            for product in products:
                asyncio.run(test_scraper(product))

        finally:
            lock.release()

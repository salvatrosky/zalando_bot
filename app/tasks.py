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
def proccess_link(product_id, first_time=False):
    from app.models import Product
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return 
    
    result = asyncio.run(test_scraper(product, first_time))
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

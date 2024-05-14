from __future__ import absolute_import, unicode_literals
from celery import shared_task
import asyncio
from app.zalando_scrapper import test_scraper
import logging

logger = logging.getLogger(__name__)

@shared_task
def proccess_link(message, user_id):
    logger.info(f"Start proccess_link with args: {message}, {user_id}")
    result = asyncio.run(test_scraper(message, user_id))
    return result

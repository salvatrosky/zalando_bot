from django.apps import AppConfig

from app.bot.bot import run_bot
from core.settings import CONTAINER_NAME


class AppConfig(AppConfig):
    name = 'app'

    def ready(self):
        if CONTAINER_NAME == "DJANGO":
            run_bot()

from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton

from core.settings import TELEGRAM_TOKEN
async def send_message(chat_id, message):
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=chat_id, text=message)
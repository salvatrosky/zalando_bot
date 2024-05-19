import json

from telegram.ext import ContextTypes

from app.bot.enums import EventTypesEnum, LanguagesEnum
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton


async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton(
                lang.value,
                callback_data=json.dumps({
                    'event_type': EventTypesEnum.LANGUAGE_SET.value,
                    'data': lang.name
                })
            )
            for lang in LanguagesEnum
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text="Select language", reply_markup=reply_markup)

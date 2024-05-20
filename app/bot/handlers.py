import json

from telegram.ext import ContextTypes

from app.bot.enums import EventTypesEnum, LanguagesEnum
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from app.translations.translations import translator



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
    choose_language_message = translator.get_translation('choose_language')
    await update.message.reply_text(text=choose_language_message, reply_markup=reply_markup)

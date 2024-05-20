import re
import json
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler, CallbackQueryHandler

from app.bot.enums import EventTypesEnum
from app.bot.handlers import set_language
from app.tasks import proccess_link
from app.users.helpers import set_user_language
from asgiref.sync import sync_to_async
from telegram import Update
from core.settings import TELEGRAM_TOKEN
from app.translations.translations import translator

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    from app.models import User

    chat_id = update.message.chat_id
    try:
        await sync_to_async(User.objects.create)(chat_id=chat_id, first_name=update.effective_user.first_name)
    except Exception as e:
        logger.info(f"User already created: {e}")

    greeting = translator.get_translation(
        'greeting', name=update.effective_user.first_name)

    await update.message.reply_text(greeting)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat_id

    data = json.loads(query.data)
    logger.info(f'Data: {str(data)}')

    match data["event_type"]:
        case EventTypesEnum.LANGUAGE_SET.value:
            await set_user_language(data["data"], chat_id)

    await query.answer()

    thanks_message = translator.get_translation('thanks', data["data"])

    await query.edit_message_text(text=thanks_message)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    from app.models import Product, User

    message = update.message.text
    chat_id = update.message.chat_id

    logger.info(f"Link received: {message}")

    if re.match(r'^http[s]?://www.zalando.it', message):
        user = await sync_to_async(User.objects.get)(chat_id=chat_id)
        try:
            product_exists = await sync_to_async(Product.objects.filter(link=message, user_id=user.id).exists)()
            if product_exists:
                link_already_registered_message = translator.get_translation(
                    'link_already_registered', user.language)
                await update.message.reply_text(link_already_registered_message)
                return

            product = await sync_to_async(Product.objects.create)(link=message, user=user)

            link_registered_success_message = translator.get_translation(
                'link_registered_success', user.language)
            await update.message.reply_text(link_registered_success_message)

            await sync_to_async(proccess_link.delay)(product.id, first_time=True)

        except Exception as e:
            logger.error(f"Error processing link: {e}")
            link_processing_error_message = translator.get_translation(
                'link_processing_error', user.language)
            await update.message.reply_text(link_processing_error_message)

    else:
        invalid_http_link_message = translator.get_translation(
            'invalid_http_link', user.language)
        await update.message.reply_text(invalid_http_link_message)


def run_bot():
    logger.info("Bot started")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("language", set_language))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(
        filters.TEXT & (~filters.COMMAND), handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

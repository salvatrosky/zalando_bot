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

    await update.message.reply_text(f'Hello {update.effective_user.first_name}! Send me your Zalando link and I\'ll inform you when the price goes down.')


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat_id

    data = json.loads(query.data)
    logger.info(f'Data: {str(data)}')

    match data["event_type"]:
        case EventTypesEnum.LANGUAGE_SET.value:
            await set_user_language(data["data"], chat_id)

    await query.answer()
    await query.edit_message_text(text="Gracias por tu respuesta!")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    from app.models import Product, User

    message = update.message.text
    chat_id = update.message.chat_id

    logger.info(f"Link received: {message}")

    if re.match(r'^http[s]?://www.zalando.it', message):
        user = await sync_to_async(User.objects.get)(chat_id=chat_id)
        try:
            # Check if the product already exists
            product_exists = await sync_to_async(Product.objects.filter(link=message, user_id=user.id).exists)()
            if product_exists:
                await update.message.reply_text('This looks like a link you already have registered')
                return

            await sync_to_async(Product.objects.create)(link=message, user=user)
            await update.message.reply_text('Link registered successfully!')

            await sync_to_async(proccess_link.delay)(message, user.id)

        except Exception as e:
            logger.error(f"Error processing link: {e}")
            await update.message.reply_text('An error occurred while processing your link. Please try again later.')

    else:
        await update.message.reply_text('Please send a valid HTTP link.')


def run_bot():
    logger.info("Bot started")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("language", set_language))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(
        filters.TEXT & (~filters.COMMAND), handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

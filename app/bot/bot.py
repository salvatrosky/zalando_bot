

import re
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler
from app.tasks import proccess_link
from asgiref.sync import sync_to_async


from telegram import Update

from core.settings import TELEGRAM_TOKEN


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    from app.models import User

    chat_id = update.message.chat_id
    try:
        await sync_to_async(User.objects.create)(chat_id=chat_id, first_name=update.effective_user.first_name)

    except Exception as e:
        print("User already created: ", str(e))
        pass
    await update.message.reply_text(f'Hello {update.effective_user.first_name}! Send me your Zalando link and I\'ll inform you when the price goes down')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    from app.models import Product, User

    message = update.message.text
    chat_id = update.message.chat_id

    print("Link received:", message)

    if re.match(r'^http[s]?://www.zalando.it', message):

        user = await sync_to_async(User.objects.get)(chat_id=chat_id)
        try:
            if await sync_to_async(Product.objects.filter(link=message, user_id=user.id).exists)():
                await update.message.reply_text('This looks like a link you already have registered')
                return
            await sync_to_async(Product.objects.create)(link=message, user=user)
            await update.message.reply_text('This looks like a link! I will now process it.')
            proccess_link.delay(message, user.id)

        except Exception as e:
            print(str(e))
            await update.message.reply_text('This looks like a link you already have registered')

    else:
        await update.message.reply_text('Please send a valid HTTP link.')


def run_bot():
    print("Bot started")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(
        filters.TEXT & (~filters.COMMAND), handle_message))

    app.run_polling()

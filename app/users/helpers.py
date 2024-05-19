from asgiref.sync import sync_to_async


async def set_user_language(language, chat_id):
    from app.models import User
    user = await sync_to_async(User.objects.get)(chat_id=chat_id)
    user.language = language
    await sync_to_async(user.save)()

    return

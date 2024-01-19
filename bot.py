
from loguru import logger
from notifiers.logging import NotificationHandler
from API import TOKEN_BOT, TOKEN_CANAL_ID

params = {
    'token': TOKEN_BOT,
    'chat_id': TOKEN_CANAL_ID
}
tg_handler = NotificationHandler(provider='telegram', defaults=params)
logger.add(tg_handler)


async def send_message(resalt):
    logger.info(resalt)



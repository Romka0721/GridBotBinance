from loguru import logger
from notifiers.logging import NotificationHandler

from API import TOKEN_BOT, TOKEN_CANAL_ID

params = {
    'token': TOKEN_BOT,
    'chat_id': TOKEN_CANAL_ID
}

tg = NotificationHandler(provider='telegram', defaults=params)
logger.add(tg, format='{message}')


def send_message(order_info):
    logger.info(order_info)

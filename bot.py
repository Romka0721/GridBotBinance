from API import TOKEN_BOT, TOKEN_CANAL_ID
import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

bot = Bot(TOKEN_BOT)
dp = Dispatcher()


@dp.message()
async def send_info(result):
    await bot.send_message(chat_id=TOKEN_CANAL_ID, text=str(result))





from API import TOKEN_BOT, TOKEN_CANAL_ID
from aiogram import Bot, Dispatcher

bot = Bot(TOKEN_BOT)
dp = Dispatcher()


@dp.message()
async def send_info(result):
    await bot.send_message(chat_id=TOKEN_CANAL_ID, text=str(result))





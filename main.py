import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from config import BOT_TOKEN
import logging
import datetime

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def get_tg_user_request_time() -> str:
    """Получаем время запроса."""
    current_time = datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    return current_time


@dp.message(CommandStart())
async def start_cmd(message: Message):
    await asyncio.sleep(1)
    logging.info(f"[Start] User {message.from_user.username} (ID: {message.from_user.id}) started the bot, date: {get_tg_user_request_time()};")
    await message.reply("Hi!")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("end bot ...")

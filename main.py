import asyncio
import logging
from aiogram import Bot, Dispatcher
from modules.handlers import router
from config import BOT_TOKEN
from modules.commands import set_commands

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def start_bot(bot: Bot):
    await set_commands(bot)


async def main():
    dp.include_router(router)
    dp.startup.register(start_bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("end bot ...")

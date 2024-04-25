import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from modules.handlers import router
from modules.commands.basic_commands import start_cmd, help_cmd, info_cmd, start_bot, stop_bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from config import BOT_TOKEN


async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    dp = Dispatcher()

    dp.include_router(router)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(start_cmd, Command(commands="start"))
    dp.message.register(help_cmd, Command(commands="help"))
    dp.message.register(info_cmd, Command(commands="info"))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("end bot ...")

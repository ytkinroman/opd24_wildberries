import asyncio
from logging import getLogger, basicConfig, DEBUG, FileHandler, StreamHandler
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from modules.commands.basic_commands import start_cmd, help_cmd, info_cmd, start_bot, stop_bot, privacy_policy_cmd, stickers_cmd
from modules.handlers import router
from config import BOT_TOKEN


async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    dp = Dispatcher()

    dp.include_router(router)

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(start_cmd, Command(commands=["start", "run"]))
    dp.message.register(help_cmd, Command(commands=["help", "support"]))
    dp.message.register(info_cmd, Command(commands=["info", "information"]))
    dp.message.register(stickers_cmd, Command(commands=["stickers", "sticker"]))
    dp.message.register(privacy_policy_cmd, Command(commands=["privacy", "policy", "privacy_policy"]))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger = getLogger()
    LOGGER_FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    file_handler = FileHandler("logs/new_logs.log", encoding="utf-8")
    file_handler.setLevel(DEBUG)
    console_stream = StreamHandler()
    console_stream.setLevel(DEBUG)
    basicConfig(level=DEBUG, format=LOGGER_FORMAT, handlers=[file_handler, console_stream])

    try:
        asyncio.run(main())
        logger.info("Telegram bot is started")
    except KeyboardInterrupt:
        logger.info("Telegram bot is stopped")

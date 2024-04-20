import asyncio
import logging
from aiogram import Bot, Dispatcher
from modules.handlers import router
from config import BOT_TOKEN, ADMIN_ID, BOT_MESSAGE_START, BOT_MESSAGE_STOP
from modules.commands_list import set_commands
from modules.basic_commands import start_cmd, help_cmd, info_cmd, command_cmd, time_cmd, joke_cmd
from aiogram.filters import Command


async def start_bot(bot: Bot):
    await bot.send_message(ADMIN_ID, text=BOT_MESSAGE_START)
    await set_commands(bot)


async def stop_bot(bot: Bot):
    await bot.send_message(ADMIN_ID, text=BOT_MESSAGE_STOP)
    await set_commands(bot)


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(router)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(start_cmd, Command(commands="start"))
    dp.message.register(help_cmd, Command(commands="help"))
    dp.message.register(info_cmd, Command(commands="info"))
    dp.message.register(command_cmd, Command(commands="commands"))
    dp.message.register(time_cmd, Command(commands="time"))
    dp.message.register(joke_cmd, Command(commands="joke"))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("end bot ...")

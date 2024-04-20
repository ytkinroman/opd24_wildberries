from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command="start",
            description="Начать работу"
        ),
        BotCommand(
            command="help",
            description="Помощь"
        ),
        BotCommand(
            command="info",
            description="Информация"
        ),
        BotCommand(
            command="commands",
            description="Команды"
        ),
        BotCommand(
            command="time",
            description="Время"
        ),
        BotCommand(
            command="joke",
            description="Шутка"
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())

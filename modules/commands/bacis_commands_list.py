from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def basic_commands_list(bot: Bot):
    commands = [
        BotCommand(
            command="start",
            description="Начать работу"
        ),
        BotCommand(
            command="privacy",
            description="Политика конфиденциальности"
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
            command="stickers",
            description="Получить набор стикеров"
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())

import asyncio
from logging import getLogger
from aiogram import Bot
from aiogram.types import Message
from config import BOT_MESSAGE_WELCOME, BOT_MESSAGE_HELP, BOT_MESSAGE_INFORMATION, BOT_MESSAGE_START, BOT_MESSAGE_STOP, BOT_ADMIN_ID, BOT_MESSAGE_PRIVACY_POLICY, BOT_MESSAGE_GET_STICKERS_ID, BOT_MESSAGE_GET_STICKERS, BOT_MESSAGE_MARKETING_STICKERS, BOT_MESSAGE_ALERT_PRIVACY_POLICY
from modules.commands.bacis_commands_list import basic_commands_list
from modules.utils import get_random_message


logger = getLogger(__name__)


async def start_cmd(message: Message) -> None:
    await asyncio.sleep(1)
    logger.info("[COMMAND] User %s (ID: %d) started the bot" % (message.from_user.username, message.from_user.id))
    await message.reply(BOT_MESSAGE_WELCOME)
    await message.reply(BOT_MESSAGE_ALERT_PRIVACY_POLICY, parse_mode="HTML")
    await message.reply(BOT_MESSAGE_MARKETING_STICKERS)


async def help_cmd(message: Message) -> None:
    await asyncio.sleep(1)
    logger.info("[COMMAND] User %s (ID: %d) used help" % (message.from_user.username, message.from_user.id))
    await message.reply(BOT_MESSAGE_HELP)


async def info_cmd(message: Message) -> None:
    await asyncio.sleep(1)
    logger.info("[COMMAND] User %s (ID: %d) looked at the information" % (message.from_user.username, message.from_user.id))
    await message.reply(BOT_MESSAGE_INFORMATION, parse_mode="HTML")


async def start_bot(bot: Bot) -> None:
    await asyncio.sleep(1)
    logger.info("Notification about bot enablement sent to administrator")
    await bot.send_message(BOT_ADMIN_ID, text=BOT_MESSAGE_START)
    await basic_commands_list(bot)


async def stop_bot(bot: Bot) -> None:
    await asyncio.sleep(1)
    logger.info("Notification about bot disablement sent to administrator")
    await bot.send_message(BOT_ADMIN_ID, text=BOT_MESSAGE_STOP)


async def privacy_policy_cmd(message: Message) -> None:
    await asyncio.sleep(1)
    logger.info("[COMMAND] User %s (ID: %d) read the privacy policy" % (message.from_user.username, message.from_user.id))
    await message.reply(BOT_MESSAGE_PRIVACY_POLICY, parse_mode="HTML")


async def stickers_cmd(message: Message) -> None:
    await asyncio.sleep(1)
    logger.info("[COMMAND] User %s (ID: %d) get the stickers pack" % (message.from_user.username, message.from_user.id))
    await message.reply(BOT_MESSAGE_GET_STICKERS)
    await message.reply_sticker(sticker=get_random_message(BOT_MESSAGE_GET_STICKERS_ID))

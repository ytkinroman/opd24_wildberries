import asyncio
import logging
from aiogram import Bot
from aiogram.types import Message
from config import BOT_MESSAGE_WELCOME, BOT_MESSAGE_HELP, BOT_MESSAGE_INFORMATION, BOT_MESSAGE_START, BOT_MESSAGE_STOP, BOT_ADMIN_ID, BOT_MESSAGE_PRIVACY_POLICY
from modules.commands.bacis_commands_list import basic_commands_list
from modules.utils import get_tg_user_request_time


async def start_cmd(message: Message) -> None:
    await asyncio.sleep(1)
    logging.info(f"[COMMAND] User {message.from_user.username} (ID: {message.from_user.id}) started the bot, date: {get_tg_user_request_time()};")
    await message.reply(BOT_MESSAGE_WELCOME)


async def help_cmd(message: Message) -> None:
    await asyncio.sleep(1)
    logging.info(f"[COMMAND] User {message.from_user.username} (ID: {message.from_user.id}) used help, date: {get_tg_user_request_time()};")
    await message.reply(BOT_MESSAGE_HELP)


async def info_cmd(message: Message) -> None:
    await asyncio.sleep(1)
    logging.info(f"[COMMAND] User {message.from_user.username} (ID: {message.from_user.id}) looked at the information, date: {get_tg_user_request_time()};")
    await message.reply(BOT_MESSAGE_INFORMATION)


async def start_bot(bot: Bot) -> None:
    await bot.send_message(BOT_ADMIN_ID, text=BOT_MESSAGE_START)
    await basic_commands_list(bot)


async def stop_bot(bot: Bot) -> None:
    await bot.send_message(BOT_ADMIN_ID, text=BOT_MESSAGE_STOP)


async def privacy_policy_cmd(message: Message) -> None:
    logging.info(f"[COMMAND] User {message.from_user.username} (ID: {message.from_user.id}) has read the privacy policy, date: {get_tg_user_request_time()};")
    await message.reply(BOT_MESSAGE_PRIVACY_POLICY)

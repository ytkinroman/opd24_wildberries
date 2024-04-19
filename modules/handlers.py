import asyncio
import logging
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from config import BOT_MESSAGE_WELCOME, BOT_MESSAGE_HELP, BOT_MESSAGE_INFORMATION, BOT_MESSAGE_COMMAND
from modules.utils import get_tg_user_request_time

router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message):
    await asyncio.sleep(1)
    logging.info(f"[Start] User {message.from_user.username} (ID: {message.from_user.id}) started the bot, date: {get_tg_user_request_time()};")
    await message.reply(BOT_MESSAGE_WELCOME)


@router.message(Command("help"))
async def help_cmd(message: Message):
    await asyncio.sleep(1)
    logging.info(f"[Help] User {message.from_user.username} (ID: {message.from_user.id}) used help, date: {get_tg_user_request_time()};")
    await message.reply(BOT_MESSAGE_HELP)


@router.message(Command("info"))
async def info_cmd(message: Message):
    await asyncio.sleep(1)
    logging.info(f"[Information] User {message.from_user.username} (ID: {message.from_user.id}) looked at the information, date: {get_tg_user_request_time()};")
    await message.reply(BOT_MESSAGE_INFORMATION)


@router.message(Command("commands"))
async def command_cmd(message: Message):
    await asyncio.sleep(1)
    logging.info(f"[Command] User {message.from_user.username} (ID: {message.from_user.id}) looked at the commands, date: {get_tg_user_request_time()};")
    await message.reply(BOT_MESSAGE_COMMAND)


@router.message(Command("time"))
async def time_cmd(message: Message):
    await asyncio.sleep(1)
    logging.info(f"[Time] User {message.from_user.username} (ID: {message.from_user.id}) gets time, date: {get_tg_user_request_time()};")
    await message.reply(f"hi, date is now: {get_tg_user_request_time()}.")


@router.message(Command("joke"))
async def time_cmd(message: Message):
    await asyncio.sleep(1)
    logging.info(f"[Joke] User {message.from_user.username} (ID: {message.from_user.id}) looked at the joke, date: {get_tg_user_request_time()};")
    await message.reply("fuck it.")

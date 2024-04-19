import asyncio
import logging
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from config import *
from modules.utils import get_tg_user_request_time, extract_url, remove_newline, replace_emoji
from modules.WBParser import get_wb_comments

router = Router()


class StatesForm(StatesGroup):
    waiting_for_processing = State()


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


@router.message()
async def process_message(message: Message, state: FSMContext):
    url = extract_url(message.text)

    if url:
        if await state.get_state() is not None:
            await message.reply(BOT_MESSAGE_REQUEST_PROGRESS)
            return

        await state.set_state(StatesForm.waiting_for_processing)
        progress_message = await message.reply(BOT_MESSAGE_WAIT)
        asyncio.create_task(process_response(message, state, url, progress_message))
    else:
        await message.reply(BOT_MESSAGE_NO_URL)


async def process_response(message: Message, state: FSMContext, url: str, progress_message):
    comments = get_wb_comments(url, PARSER_MAX_COMMENTS)

    if len(comments) == 1:
        if comments[0] == "error1":
            logging.info(f"[Error] [WB] User {message.from_user.username} (ID: {message.from_user.id}), send message: {message.text}, description: No comments, date: {get_tg_user_request_time()};")
            await progress_message.delete()
            await asyncio.sleep(1)
            await message.reply(BOT_MESSAGE_ERROR_NO_COMMENTS)
            await state.clear()
        elif comments[0] == "error2":
            logging.info(f"[Error] [WB] User {message.from_user.username} (ID: {message.from_user.id}), send message: {message.text}, description: Invalid url, date: {get_tg_user_request_time()};")
            await progress_message.delete()
            await asyncio.sleep(1)
            await message.reply(BOT_MESSAGE_ERROR_NO_URL)
            await state.clear()
        elif comments[0] == "error3":
            logging.info(f"[Error] [WB] User {message.from_user.username} (ID: {message.from_user.id}), send message: {message.text}, description: Unkown error, date: {get_tg_user_request_time()};")
            await progress_message.delete()
            await asyncio.sleep(1)
            await message.reply(BOT_MESSAGE_ERROR_UNKOWN)
            await state.clear()
    else:
        comments = remove_newline(replace_emoji(comments))

        await asyncio.sleep(2)

        #mood = await asyncio.to_thread(neuro_classifier.classify_data, comments)

        result = f"Отлично, воооот результат:\n\n{comments[:5]}"
        result = result.rstrip(']') + ", ........"

        await message.reply(result)
        await progress_message.delete()
        await state.clear()

import asyncio
import logging
from config import *
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from modules.utils import get_tg_user_request_time, extract_url, remove_newline, replace_emoji
from modules.NeuroClassifier import NeuroClassifier
from modules.WBParser import get_wb_comments
from modules.HelpGPT import get_result_message
from modules.APIQueue import APIQueue

router = Router()
neuro_classifier = NeuroClassifier(NEURO_CLASSIFIER_PATH)
API_queue = APIQueue(GPT_TOKENS)


class StatesForm(StatesGroup):
    waiting_for_processing = State()


@router.message()
async def process_message(message: Message, state: FSMContext):
    if message.text is not None:
        await asyncio.sleep(1)
        url = extract_url(message.text)

        logging.info(f"[Information] User {message.from_user.username} (ID: {message.from_user.id}), send message: \"{message.text}\", date: {get_tg_user_request_time()};")

        if url:
            if await state.get_state() is not None:
                await message.reply(BOT_MESSAGE_REQUEST_PROGRESS)
                return

            await state.set_state(StatesForm.waiting_for_processing)
            progress_message = await message.reply(BOT_MESSAGE_WAIT)
            asyncio.create_task(process_response(message, state, url, progress_message))
        else:
            await message.reply(BOT_MESSAGE_NO_URL)
    else:
        await message.reply(BOT_MESSAGE_NO_URL)


async def process_response(message: Message, state: FSMContext, url: str, progress_message):
    comments = get_wb_comments(url, PARSER_MAX_COMMENTS)
    if len(comments) == 1:
        if comments[0] == "error1":
            logging.warning(f"[WARNING] [WB] User {message.from_user.username} (ID: {message.from_user.id}), send message: {message.text}, description: No comments, date: {get_tg_user_request_time()};")
            await progress_message.delete()
            #await asyncio.sleep(2)
            await message.reply(BOT_MESSAGE_ERROR_NO_COMMENTS)
            await state.clear()
        elif comments[0] == "error2":
            logging.warning(f"[WARNING] [WB] User {message.from_user.username} (ID: {message.from_user.id}), send message: {message.text}, description: Invalid url, date: {get_tg_user_request_time()};")
            await progress_message.delete()
            #await asyncio.sleep(2)
            await message.reply(BOT_MESSAGE_ERROR_NO_URL)
            await state.clear()
        elif comments[0] == "error3":
            logging.warning(f"[WARNING] [WB] User {message.from_user.username} (ID: {message.from_user.id}), send message: {message.text}, description: Unkown error, date: {get_tg_user_request_time()};")
            await progress_message.delete()
            #await asyncio.sleep(2)
            await message.reply(BOT_MESSAGE_ERROR_UNKOWN)
            await state.clear()
    else:
        comments = remove_newline(replace_emoji(comments))
        mood = await asyncio.to_thread(neuro_classifier.classify_data, comments[:NEURO_CLASSIFIER__MAX_COMMENTS])
        result = get_result_message(mood, API_queue)

        if result == "error3" or result == "error4":
            logging.error(f"[ERROR] [ChatGPT] User {message.from_user.username} (ID: {message.from_user.id}), send message: {message.text}, comments: {mood[:5]}..., description: Unkown ChatGPT error, date: {get_tg_user_request_time()};")
            await progress_message.delete()
            #await asyncio.sleep(1)
            await message.reply(BOT_MESSAGE_ERROR_NO_RESULT_GPT)

            # получить комменты

            await state.clear()
        else:
            logging.info(f"[RESPONSE] User {message.from_user.username} (ID: {message.from_user.id}), send message: \"{message.text}\", comments: {mood[:3]}..., result: \"{result[:125]}...\", date: {get_tg_user_request_time()};")
            await message.reply(result)
            await progress_message.delete()
            await state.clear()

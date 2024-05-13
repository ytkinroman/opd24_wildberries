import asyncio
import logging
from config import *
from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from modules.utils import get_tg_user_request_time, extract_url, remove_newline, replace_emoji, get_random_message, remove_double_spaces
from modules.NeuroClassifier import NeuroClassifier
from modules.WBParser import get_wb_comments
from modules.HelpGPT import get_result_message
from modules.APIQueue import APIQueue
from modules.JsonCreator import get_generation_json

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
            progress_message = await message.reply(get_random_message(BOT_MESSAGE_WAIT))
            asyncio.create_task(process_response(message, state, url, progress_message))
        else:
            await message.reply(get_random_message(BOT_MESSAGE_NO_URL))
    else:
        await message.reply(get_random_message(BOT_MESSAGE_NO_URL))


async def process_response(message: Message, state: FSMContext, url: str, progress_message):
    comments = get_wb_comments(url, WB_PARSER_MAX_COMMENTS)
    if len(comments) == 1:
        if comments[0] == "error1":
            logging.warning(f"[WARNING] [WB] User {message.from_user.username} (ID: {message.from_user.id}), send message: \"{message.text}\", description: \"No comments\", date: {get_tg_user_request_time()};")
            await progress_message.delete()
            # await asyncio.sleep(2)
            await message.reply(BOT_MESSAGE_ERROR_NO_COMMENTS)
            await state.clear()
        elif comments[0] == "error2":
            logging.warning(f"[WARNING] [WB] User {message.from_user.username} (ID: {message.from_user.id}), send message: \"{message.text}\", description: \"Invalid url\", date: {get_tg_user_request_time()};")
            await progress_message.delete()
            # await asyncio.sleep(2)
            await message.reply(BOT_MESSAGE_ERROR_NO_URL)
            await state.clear()
        elif comments[0] == "error3":
            logging.warning(f"[WARNING] [WB] User {message.from_user.username} (ID: {message.from_user.id}), send message: \"{message.text}\", description: \"Unkown error\", date: {get_tg_user_request_time()};")
            await progress_message.delete()
            # await asyncio.sleep(2)
            await message.reply(BOT_MESSAGE_ERROR_UNKOWN)
            await state.clear()
    else:
        comments = remove_newline(replace_emoji(comments))
        comments = remove_double_spaces(comments)

        mood = await asyncio.to_thread(neuro_classifier.classify_data, comments[:NEURO_CLASSIFIER_MAX_COMMENTS])

        result = get_result_message(mood, API_queue)

        result_file_json = await get_generation_json(str(message.from_user.username), str(message.from_user.id), mood, get_tg_user_request_time(), JSON_SAVE_PATH)

        if result == "error3" or result == "error4":
            logging.error(f"[ERROR] [ChatGPT] User {message.from_user.username} (ID: {message.from_user.id}), send message: {message.text}, comments: {mood[:5]}..., description: Unkown ChatGPT error, date: {get_tg_user_request_time()};")
            await message.reply(BOT_MESSAGE_ERROR_NO_RESULT_GPT)

            if result_file_json == "ERROR_JSON":
                logging.info(f"[ERROR] [JSON] User {message.from_user.username} (ID: {message.from_user.id}), send message: \"{message.text}\", description: User didn't get the JSON file, date: {get_tg_user_request_time()};")
            else:
                json_document = FSInputFile(path=result_file_json)
                logging.info(f"[JSON] User {message.from_user.username} (ID: {message.from_user.id}) got the json: \"{result_file_json}\", date: {get_tg_user_request_time()};")
                await message.reply_document(document=json_document, caption=f"Результат классификации тональности текста {result_file_json}")

            await progress_message.delete()
            await asyncio.sleep(1)
            await state.clear()
        else:
            # Краткая форма:
            # logging.info(f"[RESPONSE] User {message.from_user.username} (ID: {message.from_user.id}), send message: \"{message.text}\", comments: {mood[:4]}..., result: \"{result[:150]}...\", date: {get_tg_user_request_time()};")
            logging.info(f"[RESPONSE] User {message.from_user.username} (ID: {message.from_user.id}), send message: \"{message.text}\", comments: \"{mood}\", result: \"{result}\", date: {get_tg_user_request_time()};")

            await message.reply(result)

            if result_file_json == "ERROR_JSON":
                logging.info(f"[ERROR] [JSON] User {message.from_user.username} (ID: {message.from_user.id}), send message: \"{message.text}\", description: User didn't get the JSON file, date: {get_tg_user_request_time()};")
            else:
                logging.info(f"[JSON] User {message.from_user.username} (ID: {message.from_user.id}) got the json: \"{result_file_json}\", date: {get_tg_user_request_time()};")
                json_document = FSInputFile(path=result_file_json)
                await message.reply_document(document=json_document, caption=f"Результат классификации тональности текста {get_tg_user_request_time()}")

            await progress_message.delete()
            await asyncio.sleep(1)
            await state.clear()

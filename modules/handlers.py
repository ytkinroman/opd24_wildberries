import asyncio
from logging import getLogger
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


logger = getLogger(__name__)
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

        if url:
            if await state.get_state() is not None:
                await message.reply(BOT_MESSAGE_REQUEST_PROGRESS)
                logger.warning('[URL] User %s (ID: %d) submitted URL: %s' % (message.from_user.username, message.from_user.id, url))
                return

            await state.set_state(StatesForm.waiting_for_processing)
            progress_message = await message.reply(get_random_message(BOT_MESSAGE_WAIT))
            asyncio.create_task(process_response(message, state, url, progress_message))
            # logger.info('[URL] User %s (ID: %d) started processing URL: %s' % (message.from_user.username, message.from_user.id, url))
        else:
            logger.warning('[URL] User %s (ID: %d) sent message without URL: %s' % (message.from_user.username, message.from_user.id, message.text))
            await message.reply(get_random_message(BOT_MESSAGE_NO_URL))
    else:
        logger.warning('[URL] User %s (ID: %d) sent empty message' % (message.from_user.username, message.from_user.id))
        await message.reply(get_random_message(BOT_MESSAGE_NO_URL))


async def process_response(message: Message, state: FSMContext, url: str, progress_message):
    comments = get_wb_comments(url, WB_PARSER_MAX_COMMENTS)
    if len(comments) == 1:
        if comments[0] == "error1":
            logger.warning('[WB] User %s (ID: %d), send message: \"%s\", description: \"No comments\"' % (message.from_user.username, message.from_user.id, message.text))
            await progress_message.delete()
            await message.reply(BOT_MESSAGE_ERROR_NO_COMMENTS)
            await state.clear()
        elif comments[0] == "error2":
            logger.warning('[WB] User %s (ID: %d), send message: \"%s\", description: \"Invalid url\"' % (message.from_user.username, message.from_user.id, message.text))
            await progress_message.delete()
            await message.reply(BOT_MESSAGE_ERROR_NO_URL)
            await state.clear()
        elif comments[0] == "error3":
            logger.error('[WB] User %s (ID: %d), send message: \"%s\", description: \"Unkown error\"' % (message.from_user.username, message.from_user.id, message.text))
            await progress_message.delete()
            await message.reply(BOT_MESSAGE_ERROR_UNKOWN)
            await state.clear()
        elif comments[0] == "error5":
            logging.warning(f"[WARNING] [WB] User {message.from_user.username} (ID: {message.from_user.id}), send message: \"{message.text}\", description: \"Not enough reviews\", date: {get_tg_user_request_time()};")
            await progress_message.delete()
            # await asyncio.sleep(2)
            await message.reply(BOT_MESSAGE_NOT_ENOUGH_REVIEWS)
            await state.clear()
    else:
        comments = remove_newline(replace_emoji(comments))
        comments = remove_double_spaces(comments)

        mood = await asyncio.to_thread(neuro_classifier.classify_data, comments[:NEURO_CLASSIFIER_MAX_COMMENTS])

        result = get_result_message(mood, API_queue)

        result_file_json = await get_generation_json(str(message.from_user.username), str(message.from_user.id), mood, get_tg_user_request_time(), JSON_SAVE_PATH)

        if result == "error3" or result == "error4":
            logger.error('[ChatGPT] User %s (ID: %d), send message: \"%s\", description: \"Unkown ChatGPT error\"' % (message.from_user.username, message.from_user.id, message.text))
            await message.reply(BOT_MESSAGE_ERROR_NO_RESULT_GPT)

            if result_file_json == "ERROR_JSON":
                logger.error('[JSON] User %s (ID: %d), send message: \"%s\", description: \"User did not get the JSON file\"' % (message.from_user.username, message.from_user.id, message.text))
            else:
                json_document = FSInputFile(path=result_file_json)
                logger.info('[JSON] User %s (ID: %d), send message: \"%s\", got the json \"%s\"' % (message.from_user.username, message.from_user.id, message.text, result_file_json))
                await message.reply_document(document=json_document, caption=f"Результат классификации отзывов: {get_tg_user_request_time()}")

            await progress_message.delete()
            await asyncio.sleep(1)
            await state.clear()
        else:
            logger.info(f"[RESPONSE] User {message.from_user.username} (ID: {message.from_user.id}), send message: \"{message.text}\", comments: \"{mood}\", result: \"{result}\", ")

            await message.reply(result)

            if result_file_json == "ERROR_JSON":
                logger.error('[JSON] User %s (ID: %d), send message: \"%s\", description: \"User did not get the JSON file\"' % (message.from_user.username, message.from_user.id, message.text))
            else:
                logger.info('[JSON] User %s (ID: %d), send message: \"%s\", got the json \"%s\"' % (message.from_user.username, message.from_user.id, message.text, result_file_json))
                json_document = FSInputFile(path=result_file_json)
                await message.reply_document(document=json_document, caption=f"Результат классификации отзывов: {get_tg_user_request_time()}")

            await progress_message.delete()
            await asyncio.sleep(1)
            await state.clear()

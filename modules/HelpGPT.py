"""
Модуль для работы с GPT API.

Author: Al0n1
Version: 1.0.8

Description:
Этот модуль позволяет посылать запрос и получать ответ от GPT.
"""


import requests
import datetime
import tiktoken
from config import PROXY_OPENAI_URL, GPT_TEXT_TOKENS_LIMIT


INSTRUCTION = """
Я передаю тебе список содержащий словари, в которых ключ 'label' — означает тональность текста, 'score' — точность определения тональности и 'text' — означает сам комментарий. 
Твоя задача проанализировать все комментарии и вывести основные плюсы и минусы товара в виде непронумерованного списка. Твой ответ передаётся потенциальному покупателю этого товара.  

Описание товара:
1. Начните описание товара с короткого и ясного обзора.
2. Укажи основные характеристики товара.

Плюсы:
1. Перечисли только те плюсы, которые упоминаются в отзывах.
2. Ограничь количество пунктов до 3-5.

Минусы:
1. Перечисли только те минусы, которые упоминаются в отзывах.
2. Ограничь количество пунктов до 3-5.

Короткое заключение:
1. Сформулируй краткое и обобщающее заключение о товаре на основе предоставленных отзывов.

Важно: Если плюсов у товара нет, то есть если у товра нет ни одного положительного отзыва, то пиши в пункте 'Плюсы:' — "Не нашёл плюсов", точно так же с минусами 'Минусы:' — 'Не нашёл минусов'. Количество плюсов и минусов не фиксировано.
"""

ENCODER = tiktoken.encoding_for_model("gpt-3.5-turbo")


def exception_handler(exception_code: str, api_key: str = "", ex: str = ""):
    """
    Обработчик исключений для управления ошибками при взаимодействии с GPT.

    Args:
        exception_code (str): Код ошибки для определения типа исключения.
        api_key (str): API-ключ для отслеживания ошибок, связанных с запросами к GPT.
        ex (str): Дополнительная информация об исключении.

    Returns:
        None
    """
    if exception_code == "error3":
        with open(f"logs/log_GPT.txt", "a+", encoding="utf-8") as f:
            f.write(
                f"\n[Error] {datetime.datetime.today().strftime('%d-%m-%Y %H-%M')} : Exception by request to GPT!\n    {ex}\n")
    elif exception_code == "error4":
        with open(f"logs/log_GPT.txt", "a+", encoding="utf-8") as f:
            f.write(
                f"\n[Error] {datetime.datetime.today().strftime('%d-%m-%Y %H-%M')} : Exception from GPT! Current API key: [{api_key}]\n    Exception description: {ex}\n")


def split_comments(comments: list, tokens_quantity: str) -> list:
    """
    Разделяет список комментариев на подсписки, если их количество превышает лимит токенов.

    Args:
        comments (list): Список комментариев для анализа.
        tokens_quantity (str): Общее количество токенов в комментариях.

    Returns:
        list: Разделённые подсписки комментариев.
    """
    while tokens_quantity > GPT_TEXT_TOKENS_LIMIT:
        if tokens_quantity - GPT_TEXT_TOKENS_LIMIT < 500:
            comments.pop()
        else:
            comments = comments[:-10]
        tokens = ENCODER.encode(str(comments))
        tokens_quantity = len(tokens)
    return comments


def create_message(comments):
    """
    Создаёт сообщение для отправки API GPT на анализ комментариев.

    Args:
        comments (list): Список комментариев для анализа.

    Returns:
        list: Сообщение для отправки API.
    """
    messages = [
        {"role": "system", "content": INSTRUCTION},
        {"role": "user",
         "content": f"Вот список комментариев к товару, в нём указан кортеж, сначала идёт комментарий за ним предположительная тональность: {comments}",
         }
    ]
    return messages


def get_result_message(comments: list, API_queue):
    """
    Получает ответ от API GPT на основе списка комментариев.

    Args:
        comments (list): Список комментариев для анализа.
        API_queue (APIQueue): Очередь API-ключей для запросов к GPT.

    Returns:
        str: Ответ от GPT или код ошибки.
    """
    chat_response = None
    if comments is not None:
        try:
            tokens = ENCODER.encode(str(comments))
            tokens_quantity = len(tokens)

            if tokens_quantity > GPT_TEXT_TOKENS_LIMIT:
                comments = split_comments(comments, tokens_quantity)

            message = create_message(comments)
            number_of_attempt = 0

            while True:
                number_of_attempt += 1
                api_key = API_queue.get_head()

                response = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={"messages": message, "model": "gpt-3.5-turbo"},
                    proxies={"http": PROXY_OPENAI_URL, "https": PROXY_OPENAI_URL}
                )

                response_data = response.json()
                if "choices" in response_data and response_data["choices"] is not None:
                    chat_response = response_data["choices"][0]["message"]["content"]
                    break
                elif "error" in response_data:
                    exception_handler(exception_code="error4", api_key=api_key, ex=response_data['error']['message'])  # ГПТ вернул ошибку
                    if number_of_attempt <= len(API_queue.get_queue()):
                        API_queue.move_head_to_tail()
                    else:
                        return "error4"
        except Exception as ex:
            exception_handler(exception_code="error3", ex=ex)  # Код завершился с ошибкой
            return "error3"
    return chat_response

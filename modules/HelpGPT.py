"""
Модуль для работы с GPT API.

Author: Al0n1
Version: 1.0.2

Description:
Этот модуль позволяет посылать запрос и получать ответ от GPT.
"""


import requests
import datetime
import tiktoken
from config import PROXY_OPENAI_URL


INSTRUCTION = """Я передаю тебе список содержащий словари, в которых ключ 'label' — означает тональность текста, 'score' — точность определения тональности и 'text' — означает сам комментарий. 
Твоя задача проанализировать все комментарии и вывести из этих комментариев основные плюсы и минусы товара в виде непронумерованного списка. 
Шаблон ответа:
    Здесь небольшое описание продукта
    уйх
    Плюсы:
    1. 
    2.
    ...
    
    Минусы:
    1.
    2.
    ...
    
    Здесь короткое заключение

Количество плюсов и минусов указано для примера, реальное колличество на твоё усмотрение. Список должен быть строго нумерованный.
Следи, чтобы в твоём ответе не было противоречий, то что указано в плюсах не может фигурировать в минусах и наоборот.
Выбирать что является плюсом, а что минусом, следует по количеству упоминаний в комментариях. То есть, если что-то больше хвалят, чем ругают, то это плюс, иначе минус. 
Твой ответ должен содержать краткое общее описание, чуть более подробное описание каждого плюса и минуса в виде пронумерованного списка и краткое заключение.
В своём ответе можешь противпоставлять некоторые факты друг другу, например большинство клиентов говорят, что размер идеальный, но некоторые говорят, что размер не подошёл, можешь их противопоставить:  "В основном все хвалят размер, потому что он им подошёл, но есть часть клиентов, которым размер не подошёл.".
Не пытайся юлить, будь честен и говори прямо, ведь если ты будешь юлить, то это будет значить, что ты обманываешь наших клиентов.
Твой ответ должен содержать МАКСИМУМ 200 слов. Переноси текст в ответе на новую строку, только если это новый абзац."""

TOKENS_LIMIT = 10000
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
    while tokens_quantity > TOKENS_LIMIT:
        if tokens_quantity - TOKENS_LIMIT < 500:
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

            if tokens_quantity > TOKENS_LIMIT:
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

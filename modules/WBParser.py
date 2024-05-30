"""
Модуль для работы с Wildberries API.

Author: Al0n1
Version: 1.0.4

Description:
Этот модуль позволяет получать отзывы о товарах с сайта Wildberries.
"""


import requests
import json
import time
from .utils import get_tg_user_request_time


def remove_params(url: str) -> str:
    for char in url:
        if char == "?":
            parameter = url.index(char)
            url = url[:parameter]
            break
    return url


class WB:
    """
    Класс для работы с Wildberries API и получения отзывов о товарах.

    Attributes:
        __url (str): URL-адрес товара на сайте Wildberries.
        __headers (dict): Заголовки для запросов к API.
        __article (str): Артикул товара.
        __ImtId (str): Идентификатор товара в системе Wildberries.
        __feedbacks (list): Список отзывов о товаре.
        __raw_data (str): Сырые данные ответа от API.
        __attempt (int): Номер попытки получения данных от API.
    """

    def __init__(self, url: str):
        self.__headers: dict = {
            'Accept': '*/*',
            'Accept-Language': 'ru,en;q=0.9,ja;q=0.8,fr;q=0.7',
            'Connection': 'keep-alive',
            'Origin': 'https://www.wildberries.ru',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.5.729 (beta) Yowser/2.5 Safari/537.36',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "YaBrowser";v="23"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        self.__url: str = url
        self.__article = None
        self.__ImtId = None
        self.__feedbacks: list = []
        self.__raw_data: str = None
        self.__attempt: int = 1

    def get_url(self) -> str:
        return self.__url

    def get_article(self) -> str:
        return self.__article

    def get_ImtId(self) -> str:
        return self.__ImtId

    def get_raw_data(self) -> str:
        return self.__raw_data

    def get_feedbacks(self) -> list:
        return self.__feedbacks

    def get_headers(self) -> dict:
        return self.__headers

    def get_attempt(self) -> int:
        return self.__attempt

    def set_raw_data(self, data: str):
        self.__raw_data = data

    def set_feedbacks(self, data: list):
        self.__feedbacks = data

    def set_headers(self, new_headers: dict):
        keys = new_headers.keys()
        for key in keys:
            self.get_headers()[key] = new_headers[key]

    def set_article(self):
        self.__article: str = self.get_article_from_url()

    def set_ImtId(self):
        self.__ImtId: str = self.get_ImtId_from_API()

    def raise_attempt(self):
        self.__attempt += 1

    def get_article_from_url(self) -> str:
        counter_of_slashs = 0
        article = ""
        for char in self.get_url():
            if char == "/":
                counter_of_slashs += 1
            if 4 <= counter_of_slashs < 5 and char != "/":
                article += char
        return article

    def get_ImtId_from_API(self) -> str:
        """
        Получает идентификатор товара (ImtId) из API Wildberries.

        Метод отправляет запрос к API Wildberries для получения информации о товаре по его артикулу.
        Затем извлекает идентификатор товара (ImtId) из ответа API.

        Returns:
            str: Идентификатор товара (ImtId) или пустая строка, если идентификатор не найден.
        """

        # Установка заголовков для запроса
        headers = {
            'Authority': 'basket-12.wbbasket.ru',
            'Referer': f'https://www.wildberries.ru/catalog/{self.get_article()}/detail.aspx',
        }
        self.set_headers(headers)

        # Отправка запроса к API Wildberries для получения данных о товаре
        response = requests.get(f'https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-5819002&spp=30&nm={self.get_article()}',
                                headers=self.get_headers())

        # Проверка статуса ответа от API
        if response.status_code != 200:
            return ""
        else:
            # Извлечение идентификатора товара из ответа API
            return str(response.json()['data']['products'][0]['root']) if len(
                response.json()['data']['products']) > 0 else ""

    def filter_feedbacks(self, feedbacks: list, size: int):
        filtered_feedbacks = []
        counter = 0
        for feedback in feedbacks:
            if counter >= size:
                break
            filtered_feedbacks.append(feedback['text'])
            counter += 1
        self.set_feedbacks(filtered_feedbacks)

    def parse(self) -> requests:
        """
            Выполняет запрос к API Wildberries для получения отзывов о товаре.

            Метод отправляет GET-запрос к API Wildberries для получения отзывов о товаре по его идентификатору (ImtId).
            Затем извлекает данные о отзывах из ответа API.

            Returns:
                requests: Ответ от API Wildberries.
            """

        # Установка заголовков для запроса
        headers = {
            'Referer': self.__url,
            'Authority': "",
        }
        self.set_headers(headers)

        # Отправка запроса к API Wildberries для получения отзывов о товаре
        response = requests.get(f'https://feedbacks{self.get_attempt()}.wb.ru/feedbacks/v1/{self.get_ImtId()}',
                                headers=self.get_headers())

        return response


def exception_handler(wb: WB, exception_code: str, url: str, ex: str = "", number_of_attempt: int = 1):
    """
    Обработчик исключений при работе с Wildberries API.

    Args:
        wb (WB): Объект класса WB, с которым связано исключение.
        exception_code (str): Код исключения для определения типа ошибки.
        url (str): URL-адрес товара, к которому производится запрос.
        ex (str): Дополнительная информация об исключении.
        number_of_attempt (int): Номер попытки запроса к API.

    Returns:
        None
    """

    """if exception_code == "error2":
        with open(f"logs/log_WB.txt", "a+", encoding="utf-8") as f:
            f.write(
                f"\n[Error] [{get_tg_user_request_time()}] | Invalid URL: '{url}'\n")"""

    if exception_code == "error1":
        """with open(f"logs/log_WB.txt", "a+", encoding="utf-8") as f:
            f.write(
                f"\n[Error] [{get_tg_user_request_time()}] | No comments! URL: '{url}'\n")"""
        wb.set_feedbacks(["error1"])

    elif exception_code == "error3":
        with open(f"logs/log_WB.txt", "a+", encoding="utf-8") as f:
            f.write(
                f"\n[Error] [{get_tg_user_request_time()}] | Exception by refactoring answer from API Wildberries! URL: '{url}'\n   Exception description: {ex}\n")
        wb.set_feedbacks(["error3"])

    else:
        with open(f"logs/log_WB.txt", "a+", encoding="utf-8") as f:
            f.write(
                f"\n[Info] [{get_tg_user_request_time()}] : Status of request to API: {exception_code}! Number of attempt: {number_of_attempt}. URL: '{url}'\n")
        wb.raise_attempt()
        time.sleep(1)


def check_url(url: str, wb: WB) -> bool:
    """
    Проверяет корректность URL-адреса товара на сайте Wildberries.

    Args:
        url (str): URL-адрес товара на сайте Wildberries.
        wb (WB): Объект класса WB, с которым связана проверка.

    Returns:
        bool: Результат проверки корректности URL-адреса.
    """

    ImtId_exist = False
    its_wildberries = url.startswith("https://www.wildberries.ru/catalog/") or url.startswith("https://wildberries.ru/catalog/")

    wb.set_article()
    article_is_digit = wb.get_article().isdigit()

    if article_is_digit:
        wb.set_ImtId()
        ImtId_exist = True if wb.get_ImtId() != "" else False

    if its_wildberries and article_is_digit and ImtId_exist:
        return True
    else:
        #exception_handler(wb, exception_code="error2", url=url)
        return False


def get_wb_comments(url: str, size: int = 10) -> list:
    """
    Получает отзывы о товаре с сайта Wildberries.

    Args:
        url (str): URL-адрес товара на сайте Wildberries.
        size (int): Количество отзывов для получения.

    Returns:
        list: Список отзывов о товаре.
    """

    comments = []
    wb = WB(remove_params(url))

    if check_url(url, wb):
        wb.set_article()
        wb.set_ImtId()

        for attempt in range(1, 3):
            response = wb.parse()
            if response.status_code != 200:
                exception_handler(wb, exception_code=str(response.status_code), url=url, number_of_attempt=attempt)
            else:
                wb.set_raw_data(response.text)
                try:
                    JSON = json.loads(wb.get_raw_data())
                    JSON = JSON['feedbacks']

                    if not JSON and attempt > 1:
                        exception_handler(wb, exception_code="error1", url=url)
                        comments = wb.get_feedbacks()
                        break
                    elif not JSON:
                        wb.raise_attempt()
                        time.sleep(1)  # ожидание, так как к API разрешенно 3 запроса в секунду
                    else:
                        wb.filter_feedbacks(JSON, size)
                        comments = wb.get_feedbacks()
                        break
                except Exception as ex:
                    exception_handler(wb, exception_code="error3", url=url, ex=ex)
                    comments = wb.get_feedbacks()
    else:
        comments.append("error2")

    del wb
    return comments

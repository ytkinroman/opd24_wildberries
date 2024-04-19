import requests
import json
import datetime
import time

"""
"error1.1" - нет коментов
"error2" - не верная ссылка
"error3" - неизвестная ошибка
"400" - запрос вернул не код 200
"""


def remove_params(url: str) -> str:
    for char in url:
        if char == "?":
            parameter = url.index(char)
            url = url[:parameter]
            break
    return url


class WB:
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
        self.__article: str = self.get_article_from_url()
        self.__ImtId: str = self.get_ImtId_from_API()
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
        headers = {
            'Authority': 'basket-12.wbbasket.ru',
            'Referer': f'https://www.wildberries.ru/catalog/{self.get_article()}/detail.aspx',
        }
        self.set_headers(headers)

        response = requests.get(f'https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&nm={self.get_article()}',
                                headers=self.get_headers())
        if response.status_code != 200:
            print("Status of getting ImtId: " + str(response))
            return ""
        else:
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
        headers = {
            'Referer': self.__url,
            'Authority': "",
        }
        self.set_headers(headers)

        response = requests.get(f'https://feedbacks{self.get_attempt()}.wb.ru/feedbacks/v1/{self.get_ImtId()}',
                                headers=self.get_headers())

        return response


def exception_handler(wb: WB, exception_code: str, url: str, ex: str = "", number_of_attempt: int = 1):
    if exception_code == "error2":
        print("Указана неверная ссылка!")
        with open(f"logs/log_WB.txt", "a+", encoding="utf-8") as f:
            f.write(
                f"\n[Error] {datetime.datetime.today().strftime('%d-%m-%Y %H-%M')} : Invalid URL: '{url}'\n")

    elif exception_code == "error1":
        print("Не найдены комментарии!")
        with open(f"logs/log_WB.txt", "a+", encoding="utf-8") as f:
            f.write(
                f"\n[Error] {datetime.datetime.today().strftime('%d-%m-%Y %H-%M')} : No comments! URL: '{url}'\n")
        wb.set_feedbacks(["error1"])

    elif exception_code == "error3":
        print("Возникла ошибка при преобразовнии ответа от API. Смотри логи.")
        with open(f"logs/log_WB.txt", "a+", encoding="utf-8") as f:
            f.write(
                f"\n[Error] {datetime.datetime.today().strftime('%d-%m-%Y %H-%M')} : Exception by refactoring answer from API Wildberries! URL: '{url}'\n{ex}\n")
        wb.set_feedbacks(["error3"])

    else:
        print(f"Status of request: {exception_code}")
        with open(f"logs/log_WB.txt", "a+", encoding="utf-8") as f:
            f.write(
                f"\n[Info] {datetime.datetime.today().strftime('%d-%m-%Y %H-%M')} : Status of request to API: {exception_code}! Number of attempt: {number_of_attempt}. URL: '{url}'\n")
        wb.raise_attempt()
        time.sleep(1)


def check_url(url: str, wb: WB) -> bool:
    its_wildberries = url.startswith("https://www.wildberries.ru/catalog/") or url.startswith("https://wildberries.ru/catalog/")
    article_is_digit = wb.get_article().isdigit()
    ImtId_exist = wb.get_ImtId()

    if its_wildberries and article_is_digit and ImtId_exist:
        return True
    else:
        exception_handler(wb, exception_code="error2", url=url)
        return False


def get_wb_comments(url: str, size: int = 10) -> list:
    comments = []
    wb = WB(remove_params(url))

    if check_url(url, wb):
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
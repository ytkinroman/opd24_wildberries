from config import PROXY_USERNAME, PROXY_PASSWORD, PROXY_IP


__author__ = "@ytkinroman"
__version__ = "1.0.0"


class Proxy:
    """Класс, представляющий прокси-сервер."""

    def __init__(self) -> None:
        """Инициализирует экземпляр класса Proxy с заданными настройками."""
        self.__PROXY_LOGIN = PROXY_USERNAME
        self.__PROXY_PASSWORD = PROXY_PASSWORD
        self.__PROXY_IP = PROXY_IP
        self.__PROXY_URL = f"http://{self.__PROXY_LOGIN}:{self.__PROXY_PASSWORD}@{self.__PROXY_IP}"

    def get_urls(self) -> dict[str, str]:
        """Возвращает словарь с HTTP и HTTPS URL-адресами прокси-сервера."""
        proxies_dict = {
            "http": self.__PROXY_URL,
            "https": self.__PROXY_URL
        }
        return proxies_dict

import random
from config import BOT_MESSAGE_GET_STICKERS_ID


__version__ = "1.0.0"
__author__ = "ytkinroman"


class StickerPack:
    """Класс для управления набором стикеров."""
    def __init__(self) -> None:
        self.__stickers = BOT_MESSAGE_GET_STICKERS_ID

    def get_sticker(self) -> str:
        """Возвращает случайный стикер из набора."""
        return random.choice(self.__stickers)

"""
Класс очереди API.

Author: Al0n1
Version: 1.0.0
"""


class APIQueue:
    def __init__(self, API_list: list):
        self.__queue: list = API_list
        self.__head: str = self.__queue[0]

    def get_queue(self) -> list:
        return self.__queue

    def get_head(self) -> str:
        return self.__head

    def set_head(self, key: str):
        self.__head = key

    def set_queue(self, queue: list):
        self.__queue = queue

    def move_head_to_tail(self):
        queue: list = self.get_queue()[1:]
        head: str = self.get_head()
        queue.append(head)
        self.set_queue(queue)
        self.set_head(queue[0])

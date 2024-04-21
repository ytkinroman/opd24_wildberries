class APIQueue:
    def init(self, API_list: list):
        self.queue: list = API_list
        self.head: str = self.queue[0]

    def get_queue(self) -> list:
        return self.queue

    def get_head(self) -> str:
        return self.head

    def set_head(self, key: str):
        self.head = key

    def set_queue(self, queue: list):
        self.__queue = queue

    def move_head_to_tail(self):
        queue: list = self.get_queue()[1:]
        head: str = self.get_head()
        queue.append(head)
        self.set_queue(queue)
        self.set_head(queue[0])

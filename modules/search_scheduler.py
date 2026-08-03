import time
from queue import Queue


class SearchScheduler:

    def __init__(self):

        self.queue = Queue()

        self.total_tasks = 0

        self.completed_tasks = 0

    def add_task(
        self,
        role,
        country
    ):

        self.queue.put(
            (
                role,
                country
            )
        )

        self.total_tasks += 1

    def get_next_task(self):

        if self.queue.empty():

            return None

        return self.queue.get()

    def task_completed(self):

        self.completed_tasks += 1

    def progress(self):

        if self.total_tasks == 0:

            return 0

        return round(

            self.completed_tasks
            / self.total_tasks
            * 100,

            1

        )

    def remaining(self):

        return self.queue.qsize()

    def wait(self):

        time.sleep(0.5)
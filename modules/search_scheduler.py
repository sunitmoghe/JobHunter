import time
import threading
from queue import Queue, Empty


class SearchScheduler:

    def __init__(self):

        self.queue = Queue()

        self.total_tasks = 0
        self.completed_tasks = 0

        self.lock = threading.Lock()

    # --------------------------------------------------
    # ADD SINGLE TASK
    # --------------------------------------------------

    def add_task(
        self,
        role,
        country
    ):

        task = {

            "role": role,

            "country": country

        }

        self.queue.put(task)

        with self.lock:

            self.total_tasks += 1

        return task

    # --------------------------------------------------
    # ADD MULTIPLE TASKS
    # --------------------------------------------------

    def add_tasks(
        self,
        roles,
        countries
    ):

        added = 0

        for role in roles:

            for country in countries:

                self.add_task(
                    role,
                    country
                )

                added += 1

        return added

    # --------------------------------------------------
    # GET NEXT TASK
    # --------------------------------------------------

    def get_next_task(self):

        try:

            return self.queue.get_nowait()

        except Empty:

            return None

    # --------------------------------------------------
    # TASK COMPLETED
    # --------------------------------------------------

    def task_completed(self):

        with self.lock:

            if (
                self.completed_tasks
                <
                self.total_tasks
            ):

                self.completed_tasks += 1

        try:

            self.queue.task_done()

        except ValueError:

            pass

    # --------------------------------------------------
    # PROGRESS
    # --------------------------------------------------

    def progress(self):

        with self.lock:

            if self.total_tasks == 0:

                return 0.0

            percentage = (

                self.completed_tasks
                /
                self.total_tasks

            ) * 100

        return round(
            min(
                percentage,
                100.0
            ),
            1
        )

    # --------------------------------------------------
    # REMAINING TASKS
    # --------------------------------------------------

    def remaining(self):

        return self.queue.qsize()

    # --------------------------------------------------
    # HAS TASKS
    # --------------------------------------------------

    def has_tasks(self):

        return not self.queue.empty()

    # --------------------------------------------------
    # IS COMPLETE
    # --------------------------------------------------

    def is_complete(self):

        with self.lock:

            return (

                self.total_tasks > 0

                and

                self.completed_tasks
                >=
                self.total_tasks

            )

    # --------------------------------------------------
    # GET STATUS
    # --------------------------------------------------

    def get_status(self):

        with self.lock:

            total = self.total_tasks

            completed = self.completed_tasks

        remaining = self.remaining()

        progress = (

            round(
                (
                    completed
                    /
                    total
                )
                * 100,
                1
            )

            if total > 0

            else 0.0

        )

        return {

            "total_tasks": total,

            "completed_tasks": completed,

            "remaining_tasks": remaining,

            "progress": min(
                progress,
                100.0
            ),

            "complete": (
                total > 0
                and
                completed >= total
            )

        }

    # --------------------------------------------------
    # RESET
    # --------------------------------------------------

    def reset(self):

        while True:

            try:

                self.queue.get_nowait()

                try:

                    self.queue.task_done()

                except ValueError:

                    pass

            except Empty:

                break

        with self.lock:

            self.total_tasks = 0

            self.completed_tasks = 0

    # --------------------------------------------------
    # WAIT / RATE LIMIT
    # --------------------------------------------------

    def wait(
        self,
        seconds=0.25
    ):

        if seconds > 0:

            time.sleep(seconds)


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    scheduler = SearchScheduler()

    roles = [

        "Head of Sales",

        "Regional Sales Director",

        "VP Sales"

    ]

    countries = [

        "Singapore",

        "UAE",

        "Germany",

        "India"

    ]

    scheduler.add_tasks(
        roles,
        countries
    )

    print()

    print(
        "Total Tasks:",
        scheduler.total_tasks
    )

    print()

    while scheduler.has_tasks():

        task = scheduler.get_next_task()

        if task is None:

            break

        print(
            "Searching:",
            task["role"],
            "|",
            task["country"]
        )

        scheduler.wait(
            0.05
        )

        scheduler.task_completed()

        print(
            "Progress:",
            scheduler.progress(),
            "%"
        )

    print()

    print(
        "Final Status:"
    )

    print(
        scheduler.get_status()
    )
import threading
import time


class SearchProgress:

    def __init__(self):

        self.progress = 0

        self.status = "Idle"

        self.current_role = ""

        self.running = False

        self.lock = threading.Lock()

    def start(self):

        with self.lock:

            self.progress = 0

            self.status = "Searching..."

            self.current_role = ""

            self.running = True

    def update(
        self,
        progress,
        role=""
    ):

        with self.lock:

            self.progress = progress

            self.current_role = role

    def finish(self):

        with self.lock:

            self.progress = 100

            self.status = "Completed"

            self.running = False

    def reset(self):

        with self.lock:

            self.progress = 0

            self.status = "Idle"

            self.current_role = ""

            self.running = False

    def get_state(self):

        with self.lock:

            return {

                "progress": self.progress,

                "status": self.status,

                "current_role": self.current_role,

                "running": self.running

            }


if __name__ == "__main__":

    tracker = SearchProgress()

    tracker.start()

    for i in range(0, 101, 20):

        tracker.update(i, f"Role {i}")

        print(tracker.get_state())

        time.sleep(0.2)

    tracker.finish()

    print(tracker.get_state())
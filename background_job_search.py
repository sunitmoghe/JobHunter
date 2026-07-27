import threading
import time


class BackgroundJobSearch:

    def __init__(self):

        self.running = False

        self.completed = False

        self.jobs = []

        self.progress = 0

        self.total_roles = 0

        self.completed_roles = 0

        self.thread = None

    def start(self, agent, roles):

        if self.running:
            return

        self.running = True
        self.completed = False
        self.jobs = []
        self.progress = 0
        self.total_roles = len(roles)
        self.completed_roles = 0

        self.thread = threading.Thread(
            target=self._worker,
            args=(agent, roles),
            daemon=True
        )

        self.thread.start()

    def _worker(self, agent, roles):

        all_jobs = []

        for role in roles:

            try:

                jobs = agent.search_single_role(role)

                if jobs:

                    all_jobs.extend(jobs)

            except Exception as e:

                print(e)

            self.completed_roles += 1

            self.progress = int(
                (self.completed_roles / self.total_roles) * 100
            )

            time.sleep(0.05)

        all_jobs.sort(
            key=lambda x: x.get(
                "executive_score",
                0
            ),
            reverse=True
        )

        self.jobs = all_jobs

        self.running = False

        self.completed = True

    def get_progress(self):

        return self.progress

    def is_running(self):

        return self.running

    def is_completed(self):

        return self.completed

    def get_jobs(self):

        return self.jobs
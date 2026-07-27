class SearchState:

    def __init__(self):

        self.reset()

    def reset(self):

        self.running = False

        self.completed = False

        self.progress = 0

        self.current_role = ""

        self.jobs = []

        self.total_roles = 0

        self.completed_roles = 0

    def start(self, total_roles):

        self.running = True

        self.completed = False

        self.progress = 0

        self.jobs = []

        self.total_roles = total_roles

        self.completed_roles = 0

        self.current_role = ""

    def update_role(self, role):

        self.current_role = role

    def update_progress(self):

        self.completed_roles += 1

        if self.total_roles > 0:

            self.progress = int(

                (self.completed_roles / self.total_roles) * 100

            )

    def add_jobs(self, jobs):

        self.jobs.extend(jobs)

    def finish(self):

        self.running = False

        self.completed = True

        self.progress = 100

    def get_jobs(self):

        return self.jobs
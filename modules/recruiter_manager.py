from modules.recruiter_database import RecruiterDatabase


class RecruiterManager:


    def __init__(self):

        self.db = RecruiterDatabase()



    def add_recruiter(
        self,
        recruiter_name,
        company,
        designation,
        linkedin,
        email,
        role,
        status,
        follow_up,
        notes
    ):

        self.db.add_recruiter(
            recruiter_name,
            company,
            designation,
            linkedin,
            email,
            role,
            status,
            follow_up,
            notes
        )



    def get_recruiters(self):

        return self.db.get_recruiters()
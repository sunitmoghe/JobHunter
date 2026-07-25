class PriorityEngine:


    def calculate_priority(self, job, match_score):

        priority = match_score


        role = job["role"].lower()


        senior_roles = [
            "chief",
            "vp",
            "director",
            "head",
            "country manager"
        ]


        for level in senior_roles:

            if level in role:

                priority += 10
                break


        if job["country"] in [
            "Singapore",
            "Germany",
            "UAE",
            "Saudi Arabia"
        ]:

            priority += 5


        if priority >= 90:

            category = "🔥 Apply Immediately"

        elif priority >= 75:

            category = "⭐ High Priority"

        else:

            category = "📌 Review"


        return {

            "priority_score": min(priority,100),

            "category": category

        }
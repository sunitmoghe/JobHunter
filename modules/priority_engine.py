class PriorityEngine:


    def calculate_priority(self, job, match_score):

        priority = match_score


        role = job.get(
            "role",
            ""
        ).lower()


        country = job.get(
            "country",
            ""
        )


        senior_roles = [
            "chief",
            "cro",
            "coo",
            "vp",
            "vice president",
            "director",
            "head",
            "country manager"
        ]


        for level in senior_roles:

            if level in role:

                priority += 10
                break



        priority_countries = [
            "Singapore",
            "Germany",
            "UAE",
            "Saudi Arabia",
            "Norway",
            "Finland",
            "Netherlands",
            "Australia"
        ]


        if country in priority_countries:

            priority += 5



        if priority >= 90:

            category = "🔥 Apply Immediately"


        elif priority >= 75:

            category = "🔥 High Priority"


        else:

            category = "📌 Review"



        return {

            "priority_score": min(
                priority,
                100
            ),

            "category": category

        }
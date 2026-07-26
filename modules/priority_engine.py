class PriorityEngine:

    def calculate_priority(self, job, match_score):

        priority = float(match_score)

        role = (
            job.get("role")
            or job.get("title")
            or ""
        ).lower()

        country = job.get("country", "")

        company = job.get("company", "Unknown")

        senior_roles = [
            "chief",
            "ceo",
            "cro",
            "coo",
            "cto",
            "cfo",
            "vice president",
            "vp",
            "director",
            "head",
            "country manager",
            "general manager",
            "regional director"
        ]

        if any(level in role for level in senior_roles):
            priority += 12

        preferred_countries = [
            "Singapore",
            "Germany",
            "UAE",
            "Saudi Arabia",
            "Norway",
            "Finland",
            "Netherlands",
            "Australia",
            "United Kingdom",
            "United States"
        ]

        if country in preferred_countries:
            priority += 8

        priority = min(priority, 100)

        if priority >= 90:
            category = "🔥 Apply Immediately"

        elif priority >= 80:
            category = "⭐⭐ High Priority"

        elif priority >= 70:
            category = "⭐ Good Opportunity"

        elif priority >= 60:
            category = "📌 Worth Reviewing"

        else:
            category = "❌ Low Priority"

        return {

            "priority_score": round(priority, 2),

            "category": category,

            "company": company,

            "country": country
        }
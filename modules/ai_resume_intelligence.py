class AIResumeIntelligence:

    def analyze_profile(self, profile):

        skills = profile.get("skills", [])
        experience = profile.get("experience", "")
        current_role = profile.get("current_role", "")
        industry = profile.get("industry", "")

        positioning_score = self.calculate_score(
            skills,
            experience,
            current_role
        )

        return {

            "positioning_score": positioning_score,

            "executive_summary": self.generate_summary(
                profile
            ),

            "leadership_strengths": self.identify_strengths(
                skills
            ),

            "recommended_roles": self.recommend_roles(
                skills,
                current_role
            ),

            "keyword_gaps": self.find_keyword_gaps(
                skills
            ),

            "career_advice": self.generate_career_advice(
                positioning_score,
                industry
            )
        }

    def calculate_score(
        self,
        skills,
        experience,
        current_role
    ):

        score = 50

        score += min(len(skills) * 2, 20)

        if experience:
            score += 15

        if current_role:
            score += 10

        executive_keywords = [
            "director",
            "head",
            "vice president",
            "vp",
            "chief",
            "cro",
            "coo",
            "ceo"
        ]

        role = current_role.lower()

        if any(keyword in role for keyword in executive_keywords):
            score += 10

        return min(score, 100)

    def generate_summary(
        self,
        profile
    ):

        role = profile.get(
            "current_role",
            "Executive Leader"
        )

        industry = profile.get(
            "industry",
            "multiple industries"
        )

        experience = profile.get(
            "experience",
            "extensive"
        )

        return (
            f"{role} with {experience} experience delivering business growth, "
            f"commercial excellence and strategic transformation across {industry}. "
            f"Strong background in revenue acceleration, customer success, "
            f"operational leadership, stakeholder management and building "
            f"high-performing teams."
        )

    def identify_strengths(
        self,
        skills
    ):

        leadership_keywords = {

            "sales",
            "leadership",
            "management",
            "operations",
            "strategy",
            "revenue",
            "customer success",
            "business development",
            "crm",
            "saas",
            "forecasting",
            "negotiation",
            "partnership",
            "p&l",
            "growth",
            "enterprise sales"

        }

        strengths = []

        for skill in skills:

            if skill.lower() in leadership_keywords:
                strengths.append(skill)

        if not strengths:

            strengths.append(
                "Business Leadership"
            )

        return sorted(
            list(set(strengths))
        )

    def recommend_roles(
        self,
        skills,
        current_role
    ):

        return [

            "Chief Revenue Officer",

            "Chief Operating Officer",

            "VP Sales",

            "Regional Sales Director",

            "Country Manager",

            "Head of Business Development",

            "Head of Customer Success",

            "Commercial Director"

        ]

    def find_keyword_gaps(
        self,
        skills
    ):

        recommended = [

            "AI Transformation",

            "Digital Transformation",

            "Cloud Revenue",

            "Enterprise SaaS",

            "Executive Leadership",

            "Board Reporting",

            "Strategic Partnerships",

            "International Expansion",

            "Revenue Operations",

            "Go-To-Market Strategy"

        ]

        existing = {

            skill.lower()

            for skill in skills

        }

        gaps = []

        for keyword in recommended:

            if keyword.lower() not in existing:

                gaps.append(keyword)

        return gaps

    def generate_career_advice(
        self,
        score,
        industry
    ):

        if score >= 90:

            return (
                "Your executive profile is highly competitive. Focus on global leadership roles and tailor your resume for each opportunity."
            )

        elif score >= 75:

            return (
                "Your profile is strong. Strengthen it further by adding measurable achievements and executive-level keywords."
            )

        else:

            return (
                "Enhance your profile by quantifying business impact, highlighting strategic leadership and incorporating industry-specific executive terminology."
            )
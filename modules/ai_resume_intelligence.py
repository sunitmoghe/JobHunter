class AIResumeIntelligence:

    # --------------------------------------------------

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

            "executive_summary": self.generate_summary(profile),

            "leadership_strengths": self.identify_strengths(skills),

            "recommended_roles": self.recommend_roles(

                skills,
                current_role,
                industry

            ),

            "keyword_gaps": self.find_keyword_gaps(skills),

            "career_advice": self.generate_career_advice(

                positioning_score,
                industry

            )

        }

    # --------------------------------------------------

    def calculate_score(

        self,
        skills,
        experience,
        current_role

    ):

        score = 40

        score += min(len(skills), 20)

        try:

            years = int(

                "".join(

                    c for c in str(experience)

                    if c.isdigit()

                )

            )

        except Exception:

            years = 0

        if years >= 20:

            score += 20

        elif years >= 15:

            score += 15

        elif years >= 10:

            score += 10

        role = str(current_role).lower()

        executive_titles = [

            "head",
            "director",
            "regional",
            "vice president",
            "vp",
            "chief",
            "cro",
            "coo",
            "ceo",
            "gm",
            "general manager"

        ]

        if any(title in role for title in executive_titles):

            score += 20

        return min(score, 100)

    # --------------------------------------------------

    def generate_summary(self, profile):

        role = profile.get(

            "current_role",
            "Executive Leader"

        )

        industry = profile.get(

            "industry",
            "Technology"

        )

        experience = profile.get(

            "experience",
            "20+ years"

        )

        return (

            f"{role} with {experience} of leadership experience "

            f"driving commercial growth, operational excellence, "

            f"business transformation and customer success across "

            f"{industry}. Proven ability to build high-performance "

            f"teams, scale revenue and deliver measurable business impact."

        )

    # --------------------------------------------------

    def identify_strengths(self, skills):

        executive_skills = {

            "sales",
            "leadership",
            "operations",
            "strategy",
            "crm",
            "customer success",
            "saas",
            "forecasting",
            "negotiation",
            "enterprise sales",
            "business development",
            "digital transformation",
            "revenue growth",
            "partnerships",
            "people management",
            "p&l"

        }

        strengths = [

            skill

            for skill in skills

            if skill.lower() in executive_skills

        ]

        if not strengths:

            strengths = [

                "Business Leadership"

            ]

        return sorted(

            set(strengths)

        )

    # --------------------------------------------------

    def recommend_roles(

        self,
        skills,
        current_role,
        industry

    ):

        roles = [

            "Chief Revenue Officer",

            "Chief Operating Officer",

            "Vice President Sales",

            "Regional Sales Director",

            "Country Manager",

            "Commercial Director",

            "Head of Business Development",

            "Head of Customer Success",

            "Managing Director",

            "Business Unit Head"

        ]

        return roles

    # --------------------------------------------------

    def find_keyword_gaps(self, skills):

        recommended = [

            "AI Strategy",

            "Digital Transformation",

            "Executive Leadership",

            "Enterprise SaaS",

            "Go-To-Market Strategy",

            "Revenue Operations",

            "International Expansion",

            "Board Reporting",

            "Business Transformation",

            "Strategic Partnerships"

        ]

        existing = {

            skill.lower()

            for skill in skills

        }

        return [

            keyword

            for keyword in recommended

            if keyword.lower() not in existing

        ]

    # --------------------------------------------------

    def generate_career_advice(

        self,
        score,
        industry

    ):

        if score >= 90:

            return (

                "Executive profile is world-class. Target Global VP, CRO, COO and Country Leadership positions."

            )

        elif score >= 75:

            return (

                "Strong executive profile. Increase ATS visibility by adding measurable business outcomes and leadership keywords."

            )

        return (

            "Strengthen executive positioning with quantified achievements, international leadership exposure and executive terminology."

        )


# --------------------------------------------------

if __name__ == "__main__":

    sample_profile = {

        "current_role": "General Manager",

        "experience": "23+ Years",

        "industry": "Technology",

        "skills": [

            "Leadership",

            "CRM",

            "Revenue Growth",

            "Sales",

            "Business Development"

        ]

    }

    ai = AIResumeIntelligence()

    result = ai.analyze_profile(sample_profile)

    print()

    print(result)
class CareerStrategyAI:

    def __init__(self):

        self.market_weights = {

            "Singapore": {
                "career_fit": 95,
                "salary_fit": 92,
                "visa_fit": 90,
                "family_fit": 88,
                "market_demand": 95
            },

            "UAE": {
                "career_fit": 92,
                "salary_fit": 90,
                "visa_fit": 95,
                "family_fit": 90,
                "market_demand": 90
            },

            "Germany": {
                "career_fit": 88,
                "salary_fit": 85,
                "visa_fit": 88,
                "family_fit": 90,
                "market_demand": 85
            },

            "Netherlands": {
                "career_fit": 86,
                "salary_fit": 85,
                "visa_fit": 85,
                "family_fit": 90,
                "market_demand": 84
            },

            "Switzerland": {
                "career_fit": 85,
                "salary_fit": 98,
                "visa_fit": 70,
                "family_fit": 88,
                "market_demand": 82
            },

            "Australia": {
                "career_fit": 84,
                "salary_fit": 86,
                "visa_fit": 85,
                "family_fit": 95,
                "market_demand": 82
            },

            "Canada": {
                "career_fit": 82,
                "salary_fit": 80,
                "visa_fit": 90,
                "family_fit": 95,
                "market_demand": 80
            },

            "United Kingdom": {
                "career_fit": 82,
                "salary_fit": 82,
                "visa_fit": 80,
                "family_fit": 85,
                "market_demand": 80
            },

            "Saudi Arabia": {
                "career_fit": 80,
                "salary_fit": 92,
                "visa_fit": 95,
                "family_fit": 75,
                "market_demand": 85
            },

            "Qatar": {
                "career_fit": 78,
                "salary_fit": 90,
                "visa_fit": 95,
                "family_fit": 75,
                "market_demand": 78
            },

            "Norway": {
                "career_fit": 78,
                "salary_fit": 90,
                "visa_fit": 75,
                "family_fit": 90,
                "market_demand": 76
            },

            "Sweden": {
                "career_fit": 76,
                "salary_fit": 82,
                "visa_fit": 80,
                "family_fit": 90,
                "market_demand": 75
            },

            "Finland": {
                "career_fit": 75,
                "salary_fit": 80,
                "visa_fit": 78,
                "family_fit": 90,
                "market_demand": 74
            },

            "Denmark": {
                "career_fit": 75,
                "salary_fit": 85,
                "visa_fit": 78,
                "family_fit": 90,
                "market_demand": 74
            },

            "Poland": {
                "career_fit": 72,
                "salary_fit": 75,
                "visa_fit": 82,
                "family_fit": 80,
                "market_demand": 72
            },

            "Ireland": {
                "career_fit": 76,
                "salary_fit": 82,
                "visa_fit": 80,
                "family_fit": 85,
                "market_demand": 75
            },

            "New Zealand": {
                "career_fit": 70,
                "salary_fit": 75,
                "visa_fit": 85,
                "family_fit": 95,
                "market_demand": 70
            },

            "Malaysia": {
                "career_fit": 78,
                "salary_fit": 72,
                "visa_fit": 85,
                "family_fit": 82,
                "market_demand": 76
            },

            "Indonesia": {
                "career_fit": 75,
                "salary_fit": 70,
                "visa_fit": 80,
                "family_fit": 78,
                "market_demand": 75
            },

            "India": {
                "career_fit": 75,
                "salary_fit": 65,
                "visa_fit": 100,
                "family_fit": 95,
                "market_demand": 75
            }

        }

    def calculate_executive_score(self, profile):

        experience = profile.get("experience", 20)
        skills = profile.get("skills", [])

        try:
            experience = int(experience)
        except Exception:
            experience = 20

        leadership = 80
        revenue = 80
        global_fit = 75
        technology = 75
        market = 80

        if experience >= 20:
            leadership += 15
            revenue += 10

        keywords = [
            "saas",
            "ai",
            "iot",
            "digital",
            "cloud",
            "crm"
        ]

        for skill in skills:
            text = str(skill).lower()
            for keyword in keywords:
                if keyword in text:
                    technology += 3

        leadership = min(100, leadership)
        revenue = min(100, revenue)
        global_fit = min(100, global_fit)
        technology = min(100, technology)
        market = min(100, market)

        breakdown = {
            "leadership_score": leadership,
            "revenue_score": revenue,
            "global_fit_score": global_fit,
            "technology_score": technology,
            "market_score": market
        }

        overall = int(sum(breakdown.values()) / len(breakdown))

        return {
            "overall_score": overall,
            "breakdown": breakdown
        }

    def recommend_countries(self, profile):

        recommendations = []

        for country, data in self.market_weights.items():

            score = int(

                (
                    data["career_fit"] +
                    data["salary_fit"] +
                    data["visa_fit"] +
                    data["family_fit"] +
                    data["market_demand"]
                ) / 5

            )

            recommendations.append({

                "country": country,
                "score": score,
                "details": data

            })

        recommendations.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return recommendations

    def analyse_strengths(self, profile):

        strengths = []

        experience = profile.get("experience", 20)

        try:
            experience = int(experience)
        except Exception:
            experience = 20

        if experience >= 20:
            strengths.append(
                "23+ years executive leadership experience"
            )

        strengths.extend([
            "Revenue growth and P&L ownership",
            "Enterprise sales leadership",
            "Cross-functional transformation",
            "Large team management",
            "Strategic business development"
        ])

        return strengths

    def identify_gaps(self, profile):

        gaps = []

        skills = str(profile.get("skills", [])).lower()

        if "ai" not in skills:
            gaps.append(
                "Add AI transformation leadership keywords"
            )

        if "saas" not in skills:
            gaps.append(
                "Strengthen SaaS positioning"
            )

        if "cloud" not in skills:
            gaps.append(
                "Highlight cloud transformation experience"
            )

        gaps.append(
            "Add more quantified global achievements"
        )

        return gaps

    def generate_90_day_plan(self):

        return {

            "Month 1": [

                "Optimise LinkedIn executive branding",
                "Refresh ATS-friendly executive CV",
                "Prepare executive achievement portfolio"

            ],

            "Month 2": [

                "Apply for VP and Director roles",
                "Increase recruiter networking",
                "Prepare executive interview stories"

            ],

            "Month 3": [

                "Scale global applications",
                "Negotiate executive offers",
                "Finalise relocation planning"

            ]

        }

    def career_recommendation(self, profile):

        return {

            "executive_score":
                self.calculate_executive_score(profile),

            "best_markets":
                self.recommend_countries(profile)[:3],

            "strengths":
                self.analyse_strengths(profile),

            "gaps":
                self.identify_gaps(profile),

            "action_plan":
                self.generate_90_day_plan()

        }
class InterviewCoachAI:


    def __init__(self):

        pass



    def generate_questions(
        self,
        job
    ):

        role = job.get(
            "role",
            "Executive Role"
        )

        company = job.get(
            "company",
            "the organisation"
        )

        industry = job.get(
            "industry",
            "technology"
        )


        questions = [

            f"Tell me about your leadership journey and how it prepares you for the {role} position.",


            f"What attracted you to {company} and this executive opportunity?",


            "Describe a complex business transformation you led. What was the measurable outcome?",


            "How have you built and managed high-performing sales or operations teams?",


            "Explain your approach to achieving aggressive revenue targets.",


            "How do you create accurate forecasts and maintain pipeline discipline?",


            "Describe a situation where you managed multiple stakeholders with conflicting priorities.",


            "How do you improve customer experience while maintaining profitability?",


            "Tell me about a strategic partnership you created and the business impact.",


            f"What would be your 90-day strategy after joining {company}?"

        ]


        return questions



    def generate_star_answer(
        self,
        question,
        profile
    ):

        experience = profile.get(
            "experience",
            "23+ years"
        )


        skills = profile.get(
            "skills",
            []
        )


        skill_text = ", ".join(
            skills[:5]
        )


        return f"""
Situation:
I was responsible for driving business growth and operational excellence
across technology-enabled enterprises with {experience} of leadership experience.

Task:
The objective was to improve revenue performance, customer engagement,
team productivity and business scalability.

Action:
I developed structured strategies across sales execution, partner
ecosystems, customer success and operational governance.
My approach included data-driven decision making, KPI tracking and
cross-functional alignment.

Result:
Delivered measurable business improvements including revenue growth,
strong customer retention and improved operational efficiency.

Key Skills Applied:
{skill_text}
"""



    def evaluate_answer(
        self,
        answer
    ):

        score = 70


        if len(answer) > 200:

            score += 10


        if any(
            word in answer.lower()
            for word in [
                "revenue",
                "growth",
                "team",
                "result",
                "million",
                "crore"
            ]
        ):

            score += 10


        if any(
            word in answer.lower()
            for word in [
                "strategy",
                "leadership",
                "impact"
            ]
        ):

            score += 10



        if score > 100:

            score = 100



        return {

            "score": score,

            "strength":
                "Strong executive response with measurable impact.",

            "improvement":
                "Add more quantified achievements and business outcomes."

        }
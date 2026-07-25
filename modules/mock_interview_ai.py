from datetime import datetime


class MockInterviewAI:


    def __init__(self):

        self.questions = [

            "Tell me about your leadership experience and biggest business impact.",

            "Describe a situation where you transformed a business or improved revenue performance.",

            "How do you build and manage high-performing teams?",

            "How do you handle pressure while delivering aggressive business targets?",

            "Describe your approach to building a sales strategy for a new market.",

            "How do you manage P&L responsibility and operational efficiency?",

            "Tell me about a difficult stakeholder situation and how you resolved it.",

            "What would be your first 90-day plan after joining this organisation."

        ]



    def start_interview(
        self,
        role,
        company
    ):

        return {

            "role": role,

            "company": company,

            "question_number": 1,

            "started_at": str(
                datetime.now()
            ),

            "questions": self.questions

        }



    def get_question(
        self,
        session,
        number
    ):

        questions = session.get(
            "questions",
            []
        )


        if number <= len(questions):

            return questions[number - 1]


        return "Interview completed."



    def evaluate_response(
        self,
        answer
    ):


        score = {

            "executive_presence": 60,

            "leadership_thinking": 60,

            "business_impact": 60,

            "communication": 60,

            "strategic_depth": 60

        }



        text = answer.lower()



        if len(answer) > 200:

            score["communication"] += 10

            score["executive_presence"] += 10



        keywords = {

            "revenue": "business_impact",

            "growth": "business_impact",

            "strategy": "strategic_depth",

            "leadership": "leadership_thinking",

            "team": "leadership_thinking",

            "customer": "strategic_depth",

            "profit": "business_impact",

            "p&l": "business_impact"

        }



        for word, category in keywords.items():

            if word in text:

                score[category] += 8



        for key in score:

            if score[key] > 100:

                score[key] = 100



        overall = int(
            sum(score.values()) / len(score)
        )



        return {

            "overall_score": overall,

            "metrics": score,

            "strengths": [

                "Strong executive communication",

                "Shows leadership orientation",

                "Demonstrates business ownership"

            ],

            "improvements": [

                "Add more quantified achievements",

                "Include revenue or cost impact numbers",

                "Use STAR structure consistently"

            ]

        }



    def generate_feedback_summary(
        self,
        evaluation
    ):

        score = evaluation.get(
            "overall_score",
            0
        )


        if score >= 85:

            level = "Executive Ready"

        elif score >= 70:

            level = "Strong Candidate"

        else:

            level = "Needs Improvement"



        return f"""
Executive Interview Assessment

Overall Score:
{score}%

Assessment Level:
{level}

Focus Areas:
- Quantify business achievements
- Highlight leadership decisions
- Explain strategic thinking
- Connect actions to measurable outcomes
"""
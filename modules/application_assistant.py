class ApplicationAssistant:


    def generate_linkedin_message(
        self,
        profile,
        job
    ):

        name = profile.get(
            "name",
            "there"
        )

        role = job.get(
            "role",
            "this opportunity"
        )

        company = job.get(
            "company",
            "your organisation"
        )


        return f"""
Hi,

I recently came across the {role} opportunity at {company} and would like to express my interest.

With 23+ years of experience driving revenue growth, enterprise sales, business transformation, and leading high-performing teams across technology, SaaS, IoT, telecom and industrial solutions, I believe my background aligns well with your growth objectives.

Key strengths I bring:
• Strategic Sales Leadership
• P&L Ownership
• Enterprise & B2B Sales Growth
• Partner Ecosystem Development
• Global Team Leadership

I would appreciate the opportunity to connect and discuss how my experience can contribute to your organisation's growth.

Regards,
{name}
"""


    def generate_cover_letter(
        self,
        profile,
        job
    ):

        role = job.get(
            "role",
            "Executive Position"
        )

        company = job.get(
            "company",
            "your organisation"
        )

        experience = profile.get(
            "experience",
            "23+"
        )


        return f"""
Dear Hiring Manager,

I am writing to express my interest in the {role} position at {company}.

I bring {experience} years of leadership experience in revenue growth, strategic sales, customer success, operations excellence and business transformation across technology-driven organisations.

Throughout my career, I have successfully built sales ecosystems, managed large teams, delivered significant revenue growth and developed strategic customer relationships.

My experience includes:
• Enterprise Sales Leadership
• Revenue Growth Strategy
• P&L Management
• Channel Development
• SaaS, IoT and Technology Solutions

I am confident that my leadership experience and execution capability can contribute significantly to your organisation's continued growth.

I look forward to the opportunity to discuss my candidature.

Sincerely
"""


    def generate_interview_questions(
        self,
        job
    ):

        role = job.get(
            "role",
            "Executive Role"
        )


        return [

            f"Tell me about your experience relevant to {role}.",

            "Describe a complex sales transformation you delivered.",

            "How have you managed large revenue targets?",

            "How do you build and scale high-performing teams?",

            "Describe a challenging customer negotiation.",

            "How do you manage sales forecasting accuracy?",

            "What is your leadership philosophy?",

            "How do you approach entering new markets?",

            "What KPIs do you use to measure success?",

            "Why should we hire you for this role?"

        ]
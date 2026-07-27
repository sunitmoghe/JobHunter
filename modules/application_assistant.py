class ApplicationAssistant:

    def generate_linkedin_message(
        self,
        profile,
        job
    ):

        name = profile.get("name", "there")

        role = (
            job.get("role")
            or job.get("title")
            or "this opportunity"
        )

        company = job.get(
            "company",
            "your organisation"
        )

        industry = profile.get(
            "industry",
            "technology"
        )

        return f"""
Hi,

I recently came across the {role} opportunity at {company} and would like to express my interest.

With over 23 years of leadership experience across {industry}, SaaS, IoT, Telecom and Technology businesses, I have successfully delivered business growth, customer success and operational transformation.

Some highlights of my experience include:

• Driving multi-million revenue growth
• Leading large cross-functional teams
• Building strategic partnerships
• Managing enterprise customers
• P&L ownership
• Sales transformation
• International business expansion

I believe my experience aligns well with your organisation's growth objectives and would welcome the opportunity to connect.

Kind Regards,

{name}
"""

    def generate_cover_letter(
        self,
        profile,
        job
    ):

        role = (
            job.get("role")
            or job.get("title")
            or "Executive Position"
        )

        company = job.get(
            "company",
            "your organisation"
        )

        experience = profile.get(
            "experience",
            "23+"
        )

        industry = profile.get(
            "industry",
            "Technology"
        )

        return f"""
Dear Hiring Manager,

I am excited to apply for the {role} position at {company}.

With {experience} years of executive leadership experience across {industry}, I have consistently delivered measurable business growth through strategic planning, customer-centric leadership and operational excellence.

My experience includes:

• Revenue Growth
• Executive Leadership
• Enterprise Sales
• Strategic Partnerships
• P&L Management
• Business Transformation
• Customer Success
• Market Expansion

I am confident my leadership style, commercial acumen and execution capability would make a valuable contribution to your organisation.

Thank you for your consideration.

Sincerely,

{profile.get("name","")}
"""

    def generate_interview_questions(
        self,
        job
    ):

        role = (
            job.get("role")
            or job.get("title")
            or "Executive Role"
        )

        return [

            f"Tell us about your experience relevant to the {role} position.",

            "Describe the largest revenue target you have achieved.",

            "How do you build high-performing sales organisations?",

            "Describe a strategic business transformation you led.",

            "Tell us about a complex negotiation involving multiple stakeholders.",

            "How do you manage forecasting accuracy?",

            "How do you improve customer success at executive level?",

            "Explain your leadership philosophy.",

            "How do you manage cross-functional teams?",

            "Why should we hire you for this executive position?"

        ]

    def executive_application_checklist(self):

        return [

            "Tailor resume to the Job Description",

            "Optimise ATS keywords",

            "Prepare executive cover letter",

            "Send LinkedIn connection request",

            "Research company",

            "Research interviewer",

            "Prepare STAR stories",

            "Review financial performance of company",

            "Prepare salary expectations",

            "Follow up after application"

        ]

    def interview_tips(self):

        return [

            "Quantify achievements with measurable business impact.",

            "Emphasise leadership and strategic thinking.",

            "Use executive-level business language.",

            "Demonstrate ownership of revenue and P&L.",

            "Highlight global exposure and transformation initiatives.",

            "Prepare examples using the STAR framework."

        ]
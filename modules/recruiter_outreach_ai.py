class RecruiterOutreachAI:


    def __init__(self):

        pass



    def generate_connection_message(
        self,
        profile,
        recruiter
    ):

        name = recruiter.get(
            "name",
            "there"
        )

        company = recruiter.get(
            "company",
            "your organisation"
        )

        experience = profile.get(
            "experience",
            "20+"
        )


        return f"""
Hi {name},

I noticed your work in executive hiring at {company}.
I would like to connect and explore potential leadership opportunities.

I bring {experience}+ years of experience driving revenue growth,
sales transformation, business operations and P&L leadership across
technology-enabled enterprises.

I would appreciate staying connected and discussing opportunities
where my experience can create business impact.

Regards,
Sunit Moghe
"""



    def generate_followup_message(
        self,
        recruiter
    ):

        name = recruiter.get(
            "name",
            "there"
        )


        return f"""
Hi {name},

Hope you are doing well.

I wanted to follow up on my previous message and check if there are
any leadership opportunities aligned with my experience in revenue
growth, sales leadership and business transformation.

I would be happy to share additional details or discuss how I can
contribute to your organisation.

Looking forward to staying connected.

Regards,
Sunit Moghe
"""



    def generate_thank_you_message(
        self,
        company,
        role
    ):


        return f"""
Dear Hiring Team,

Thank you for the opportunity to discuss the {role} position at {company}.

I enjoyed learning more about your business goals, growth strategy and
future plans.

The conversation reinforced my interest in contributing my experience
in executive leadership, revenue growth, operational excellence and
business transformation.

I look forward to the next steps.

Regards,
Sunit Moghe
"""
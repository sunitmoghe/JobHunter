class ApplicationAssistant:

    def generate(
        self,
        profile,
        job,
    ):

        return self.generate_apply_package(
            profile,
            job,
        )

    # ----------------------------------------------------------

    def generate_linkedin_message(
        self,
        profile,
        job,
    ):

        return f"""
Hello,

I came across the opportunity for **{job.get('role','Executive Position')}** at **{job.get('company','your organisation')}**.

I have 23+ years of executive leadership experience across:

• Sales Leadership
• Operations
• P&L Management
• Business Transformation
• Customer Success
• Strategic Partnerships

I believe my experience aligns well with your leadership requirements and would appreciate the opportunity to connect.

Kind Regards,

{profile.get('name','')}
"""

    # ----------------------------------------------------------

    def generate_cover_letter(
        self,
        profile,
        job,
    ):

        return f"""
Dear Hiring Manager,

I am writing to express my interest in the position of **{job.get('role','Executive')}** at **{job.get('company','your organisation')}**.

Over the past 23+ years I have successfully delivered:

• Revenue Growth
• Executive Leadership
• International Expansion
• P&L Ownership
• Customer Success
• Business Transformation
• Strategic Partnerships

I would welcome the opportunity to discuss how my leadership experience can contribute to your organisation.

Kind Regards,

{profile.get('name','')}
"""

    # ----------------------------------------------------------

    def generate_recruiter_email(
        self,
        profile,
        job,
    ):

        return f"""
Subject: Application for {job.get('role','Executive Position')}

Dear Recruiter,

I recently applied for the position of **{job.get('role','Executive Position')}** at **{job.get('company','your organisation')}**.

With more than 23 years of executive leadership experience across Sales, Operations, Customer Success, Business Development and P&L Management, I believe my background aligns well with your requirements.

I would appreciate the opportunity to discuss how I can contribute to your organisation.

Kind Regards,

{profile.get('name','')}
"""
        # ----------------------------------------------------------

    def generate_followup_email(
        self,
        profile,
        job,
    ):

        return f"""
Dear Hiring Team,

I wanted to follow up regarding my application for the **{job.get('role','Executive Position')}** opportunity.

I remain extremely interested in joining **{job.get('company','your organisation')}** and would appreciate the opportunity to discuss my candidature.

Thank you for your consideration.

Kind Regards,

{profile.get('name','')}
"""

    # ----------------------------------------------------------

    def generate_thank_you_email(
        self,
        profile,
        job,
    ):

        return f"""
Dear Interview Panel,

Thank you for taking the time to interview me for the **{job.get('role','Executive Position')}** opportunity.

I enjoyed our discussion and remain excited about the possibility of contributing to **{job.get('company','your organisation')}**.

I appreciate your time and consideration.

Kind Regards,

{profile.get('name','')}
"""

    # ----------------------------------------------------------

    def generate_hr_email(
        self,
        profile,
        job,
    ):

        return f"""
Subject: Executive Application - {job.get('role','Executive Position')}

Dear HR Team,

Please accept my application for the position of **{job.get('role','Executive Position')}**.

I bring more than 23 years of leadership experience across Sales, Business Development, Operations, Customer Success and P&L Management.

I would welcome the opportunity to discuss how my experience can contribute to **{job.get('company','your organisation')}**.

Regards,

{profile.get('name','')}
"""

    # ----------------------------------------------------------

    def generate_hiring_manager_email(
        self,
        profile,
        job,
    ):

        return f"""
Dear Hiring Manager,

I am excited to apply for the **{job.get('role','Executive Position')}** opportunity.

My executive leadership background includes:

• Revenue Growth
• Commercial Leadership
• Strategic Partnerships
• Customer Success
• P&L Ownership
• Large Team Management

I look forward to discussing how I can help accelerate growth for **{job.get('company','your organisation')}**.

Regards,

{profile.get('name','')}
"""

    # ----------------------------------------------------------

    def executive_pitch(
        self,
        profile,
        job,
    ):

        return f"""
Executive Leader with 23+ years delivering revenue growth, commercial transformation, customer success, strategic partnerships and P&L ownership across global markets.

Interested in contributing to **{job.get('company','your organisation')}** as **{job.get('role','Executive')}**.

Immediate Joiner.
"""
        # ----------------------------------------------------------

    def generate_interview_questions(
        self,
        job,
    ):

        return [

            "Describe your biggest executive achievement.",

            "How have you delivered revenue growth?",

            "Describe a business turnaround you personally led.",

            "Explain your executive leadership philosophy.",

            "Describe your P&L ownership experience.",

            "How do you build high-performing leadership teams?",

            "Describe a strategic partnership you developed.",

            "How do you manage enterprise customers?",

            "Describe a difficult board-level decision.",

            "Why should we hire you for this executive role?",

        ]

    # ----------------------------------------------------------

    def executive_application_checklist(
        self,
    ):

        return [

            "Resume Tailored",

            "ATS Optimized",

            "Executive Cover Letter Generated",

            "LinkedIn Message Ready",

            "Recruiter Email Ready",

            "HR Email Ready",

            "Hiring Manager Email Ready",

            "Executive Pitch Ready",

            "Company Research Completed",

            "Leadership Stories Prepared",

            "Interview Questions Practiced",

            "Follow-up Email Prepared",

        ]

    # ----------------------------------------------------------

    def interview_tips(
        self,
    ):

        return [

            "Quantify every achievement with numbers.",

            "Demonstrate strategic thinking.",

            "Show leadership impact.",

            "Explain business outcomes instead of activities.",

            "Focus on commercial value creation.",

            "Use STAR examples.",

            "Explain change management experience.",

            "Highlight international exposure.",

            "Discuss customer success initiatives.",

            "Finish every answer with measurable results.",

        ]

    # ----------------------------------------------------------

    def generate_apply_package(
        self,
        profile,
        job,
    ):

        return {

            "linkedin_message":
                self.generate_linkedin_message(
                    profile,
                    job,
                ),

            "cover_letter":
                self.generate_cover_letter(
                    profile,
                    job,
                ),

            "recruiter_email":
                self.generate_recruiter_email(
                    profile,
                    job,
                ),

            "hr_email":
                self.generate_hr_email(
                    profile,
                    job,
                ),

            "hiring_manager_email":
                self.generate_hiring_manager_email(
                    profile,
                    job,
                ),

            "executive_pitch":
                self.executive_pitch(
                    profile,
                    job,
                ),

            "follow_up":
                self.generate_followup_email(
                    profile,
                    job,
                ),

            "thank_you":
                self.generate_thank_you_email(
                    profile,
                    job,
                ),

            "interview_questions":
                self.generate_interview_questions(
                    job,
                ),

            "application_checklist":
                self.executive_application_checklist(),

            "interview_tips":
                self.interview_tips(),

        }
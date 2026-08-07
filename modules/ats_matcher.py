import json
import os
import re


class ATSMatcher:

    def __init__(
        self,
        resume_text,
        job_description
    ):

        self.resume_text = str(resume_text).lower()
        self.job_description = str(job_description).lower()

        self.skills = self.load_skills()

    # --------------------------------------------------

    def load_skills(self):

        skills_path = os.path.join(
            "resources",
            "skills.json"
        )

        try:

            with open(
                skills_path,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except Exception:

            return {}

    # --------------------------------------------------

    def extract_job_keywords(self):

        words = re.findall(
            r"[a-zA-Z][a-zA-Z0-9\-\+#\.]{2,}",
            self.job_description
        )

        ignore = {
            "and", "the", "with", "from", "into", "that",
            "this", "your", "their", "will", "have", "has",
            "for", "you", "our", "are", "was", "were",
            "should", "must", "can", "able", "using",
            "required", "preferred", "experience",
            "skills", "skill", "years", "year",
            "role", "position", "team", "business",
            "company", "customer", "customers",
            "management", "manager"
        }

        keywords = []

        for word in words:

            word = word.lower()

            if word not in ignore and len(word) > 3:

                keywords.append(word)

        return sorted(set(keywords))

    # --------------------------------------------------

    def calculate_match(self):

        matched = []
        missing = []

        # ---------------------------------------
        # Skill library matching
        # ---------------------------------------

        for category, skill_list in self.skills.items():

            for skill in skill_list:

                skill_lower = skill.lower()

                if skill_lower not in self.job_description:

                    continue

                item = {

                    "category": category,
                    "skill": skill

                }

                if skill_lower in self.resume_text:

                    matched.append(item)

                else:

                    missing.append(item)

        # ---------------------------------------
        # Dynamic keyword matching
        # ---------------------------------------

        dynamic_keywords = self.extract_job_keywords()

        dynamic_missing = []

        for keyword in dynamic_keywords:

            if keyword not in self.resume_text:

                dynamic_missing.append(keyword)

        # ---------------------------------------

        total = len(matched) + len(missing)

        score = round(

            (len(matched) / total) * 100,

            2

        ) if total else 0

        interview_probability = min(

            100,

            round(score + 10)

        )

        return {

            "score": score,

            "matched": matched,

            "missing": missing,

            "matched_count": len(matched),

            "missing_count": len(missing),

            "interview_probability": interview_probability,

            "dynamic_missing_keywords": dynamic_missing[:30],

            "recommendations": self.generate_recommendations(

                score,
                matched,
                missing,
                dynamic_missing

            )

        }

    # --------------------------------------------------

    def generate_recommendations(

        self,
        score,
        matched,
        missing,
        dynamic_missing

    ):

        recommendations = []

        if missing:

            recommendations.append(

                "Add these ATS skills: "

                + ", ".join(

                    item["skill"]

                    for item in missing[:15]

                )

            )

        if dynamic_missing:

            recommendations.append(

                "Include these JD keywords where appropriate: "

                + ", ".join(dynamic_missing[:20])

            )

        recommendations.append(

            "Quantify achievements with revenue, growth %, savings, customer impact and team size."

        )

        recommendations.append(

            "Mirror the exact wording used in the job description."

        )

        recommendations.append(

            "Mention relevant tools, platforms, certifications and technologies."

        )

        recommendations.append(

            "Use strong action verbs and measurable business outcomes."

        )

        if score >= 90:

            recommendations.append(

                "Excellent ATS compatibility."

            )

        elif score >= 75:

            recommendations.append(

                "Strong ATS compatibility. Small improvements can increase interview chances."

            )

        else:

            recommendations.append(

                "Resume should be tailored before applying."

            )

        return recommendations


# --------------------------------------------------

if __name__ == "__main__":

    sample_resume = """
    Sales Director
    CRM
    Salesforce
    Strategic Sales
    Revenue Growth
    P&L
    """

    sample_jd = """
    Looking for Head of Sales with Salesforce,
    CRM, Forecasting, Revenue Growth,
    Strategic Leadership, AI, SaaS,
    Customer Success and Executive Leadership.
    """

    matcher = ATSMatcher(

        sample_resume,
        sample_jd

    )

    result = matcher.calculate_match()

    print(result)
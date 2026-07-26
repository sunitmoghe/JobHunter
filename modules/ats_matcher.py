import json
import os


class ATSMatcher:

    def __init__(self, resume_text, job_description):
        self.resume_text = resume_text.lower()
        self.job_description = job_description.lower()
        self.skills = self.load_skills()

    def load_skills(self):
        skills_path = os.path.join("resources", "skills.json")

        with open(skills_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def calculate_match(self):

        matched = []
        missing = []

        for category, skill_list in self.skills.items():

            for skill in skill_list:

                resume_has = skill.lower() in self.resume_text
                jd_needs = skill.lower() in self.job_description

                if jd_needs:

                    if resume_has:
                        matched.append(
                            {
                                "category": category,
                                "skill": skill
                            }
                        )

                    else:
                        missing.append(
                            {
                                "category": category,
                                "skill": skill
                            }
                        )

        total = len(matched) + len(missing)

        score = round((len(matched) / total) * 100, 2) if total else 0

        interview_probability = min(
            100,
            round(score + 10)
        )

        recommendations = self.generate_recommendations(
            score,
            matched,
            missing
        )

        return {
            "score": score,
            "matched": matched,
            "missing": missing,
            "interview_probability": interview_probability,
            "recommendations": recommendations
        }

    def generate_recommendations(
        self,
        score,
        matched,
        missing
    ):

        recommendations = []

        missing_skills = [
            item["skill"]
            for item in missing
        ]

        if missing_skills:

            recommendations.append(
                "Add these important keywords where they genuinely match your experience: "
                + ", ".join(missing_skills[:15])
            )

        if score < 60:

            recommendations.append(
                "Rewrite your Professional Summary to closely match the language used in the job description."
            )

        recommendations.append(
            "Quantify your achievements using measurable business results such as revenue, growth %, cost savings, customer acquisition, project value or team size."
        )

        recommendations.append(
            "Use the same terminology and keywords as the job description wherever they accurately reflect your experience."
        )

        recommendations.append(
            "Include relevant tools, technologies, certifications and industry-specific keywords mentioned in the job description."
        )

        if score >= 90:

            recommendations.append(
                "Excellent ATS alignment. Only minor refinements are recommended before applying."
            )

        elif score >= 75:

            recommendations.append(
                "Strong ATS match. Adding the remaining missing keywords can further improve your chances."
            )

        else:

            recommendations.append(
                "Tailor this resume specifically for this role before submitting your application."
            )

        return recommendations
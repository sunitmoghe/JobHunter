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
                        matched.append({
                            "category": category,
                            "skill": skill
                        })
                    else:
                        missing.append({
                            "category": category,
                            "skill": skill
                        })

        total = len(matched) + len(missing)

        score = round((len(matched) / total) * 100, 2) if total else 0

        return {
            "score": score,
            "matched": matched,
            "missing": missing
        }
import re


class JobSkillMatcher:

    def extract_matching_skills(
        self,
        resume_skills,
        job_description
    ):

        resume = {
            s.lower()
            for s in resume_skills
        }

        text = job_description.lower()

        matched = []

        missing = []

        words = set(
            re.findall(
                r"[a-zA-Z0-9+#.-]+",
                text
            )
        )

        for skill in resume:

            if skill in words:

                matched.append(skill.title())

        for word in words:

            if (
                len(word) > 3
                and word not in resume
            ):

                missing.append(word.title())

        return {

            "matched": sorted(
                list(set(matched))
            ),

            "missing": sorted(
                list(set(missing))
            )[:20]
        }

    def interview_probability(
        self,
        executive_fit
    ):

        probability = min(
            round(
                executive_fit * 0.92
            ),
            99
        )

        return probability
import re


class JobSkillMatcher:

    def extract_matching_skills(
        self,
        resume_skills,
        job_description
    ):

        resume = {
            s.lower().strip()
            for s in resume_skills
        }

        jd = job_description.lower()

        matched = []
        missing = []

        words = set(
            re.findall(
                r"[a-zA-Z0-9+#.-]+",
                jd
            )
        )

        for skill in sorted(resume):

            if skill in jd:
                matched.append(skill.title())

        for word in sorted(words):

            if (
                len(word) > 3
                and word not in resume
                and word.isalpha()
            ):
                missing.append(word.title())

        missing = missing[:20]

        score = 0

        if matched or missing:

            score = round(
                (len(matched) /
                 (len(matched) + len(missing))) * 100,
                2
            )

        return {

            "match_score": score,

            "matched": matched,

            "missing": missing,

            "interview_probability":
                self.interview_probability(score)
        }

    def interview_probability(
        self,
        score
    ):

        if score >= 90:
            return 95

        elif score >= 80:
            return 90

        elif score >= 70:
            return 82

        elif score >= 60:
            return 70

        return 55
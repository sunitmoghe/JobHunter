class JobSkillMatcher:

    def __init__(self):
        pass

    def normalize_skill(self, skill):

        if skill is None:
            return ""

        return str(skill).strip().lower()

    def get_profile_skills(self, profile):

        if not isinstance(profile, dict):
            return []

        skills = profile.get(
            "skills",
            []
        )

        if not isinstance(skills, list):
            return []

        result = []

        for skill in skills:

            normalized = self.normalize_skill(
                skill
            )

            if normalized and normalized not in result:
                result.append(normalized)

        return result

    def extract_job_text(self, job):

        if not isinstance(job, dict):
            return ""

        fields = [
            "title",
            "role",
            "job_title",
            "description",
            "summary",
            "requirements",
            "responsibilities",
            "skills",
            "keywords",
        ]

        parts = []

        for field in fields:

            value = job.get(
                field,
                ""
            )

            if isinstance(value, list):

                parts.extend(
                    str(item)
                    for item in value
                )

            elif isinstance(value, dict):

                parts.extend(
                    str(item)
                    for item in value.values()
                )

            elif value:

                parts.append(
                    str(value)
                )

        return " ".join(parts).lower()

    def get_required_skills(self, job):

        if not isinstance(job, dict):
            return []

        skills = []

        for field in [
            "skills",
            "required_skills",
            "keywords",
        ]:

            value = job.get(
                field,
                []
            )

            if isinstance(value, list):

                skills.extend(value)

            elif isinstance(value, str):

                skills.extend(
                    value.replace(
                        ",",
                        "\n"
                    ).splitlines()
                )

        result = []

        for skill in skills:

            normalized = self.normalize_skill(
                skill
            )

            if normalized and normalized not in result:
                result.append(normalized)

        return result

    def skill_matches_text(
        self,
        skill,
        job_text
    ):

        normalized_skill = self.normalize_skill(
            skill
        )

        normalized_text = str(
            job_text
        ).lower()

        if not normalized_skill:
            return False

        return normalized_skill in normalized_text

    def calculate_match(
        self,
        profile,
        job
    ):

        profile_skills = self.get_profile_skills(
            profile
        )

        job_text = self.extract_job_text(
            job
        )

        required_skills = self.get_required_skills(
            job
        )

        matched_skills = []

        missing_skills = []

        for skill in required_skills:

            if skill in profile_skills:

                if self.skill_matches_text(
                    skill,
                    job_text
                ):

                    matched_skills.append(
                        skill
                    )

            else:

                missing_skills.append(
                    skill
                )

        profile_matches = []

        for skill in profile_skills:

            if self.skill_matches_text(
                skill,
                job_text
            ):

                profile_matches.append(
                    skill
                )

        if required_skills:

            score = (
                len(matched_skills)
                / len(required_skills)
            ) * 100

        elif profile_matches:

            score = 100.0

        else:

            score = 0.0

        return {
            "match_score": round(
                score,
                2
            ),
            "matched_skills": sorted(
                matched_skills
            ),
            "missing_skills": sorted(
                missing_skills
            ),
            "profile_matches": sorted(
                profile_matches
            ),
            "required_skills": sorted(
                required_skills
            ),
        }

    def match(
        self,
        profile,
        job
    ):

        return self.calculate_match(
            profile,
            job
        )

    def score(
        self,
        profile,
        job
    ):

        result = self.calculate_match(
            profile,
            job
        )

        return result.get(
            "match_score",
            0
        )

    def get_matched_skills(
        self,
        profile,
        job
    ):

        result = self.calculate_match(
            profile,
            job
        )

        return result.get(
            "matched_skills",
            []
        )

    def get_missing_skills(
        self,
        profile,
        job
    ):

        result = self.calculate_match(
            profile,
            job
        )

        return result.get(
            "missing_skills",
            []
        )
from modules.job_skill_matcher import JobSkillMatcher


class JobMatcherEngine:

    def __init__(self):

        self.skill_matcher = JobSkillMatcher()

    def match_job(
        self,
        profile,
        job,
    ):

        result = self.skill_matcher.match(
            profile,
            job,
        )

        score = result.get(
            "match_score",
            0,
        )

        if score >= 80:

            recommendation = "Excellent Match"

        elif score >= 65:

            recommendation = "Strong Match"

        elif score >= 50:

            recommendation = "Potential Match"

        elif score >= 30:

            recommendation = "Weak Match"

        else:

            recommendation = "Low Match"

        result["recommendation"] = recommendation

        result["job_title"] = job.get(
            "title",
            job.get(
                "role",
                job.get(
                    "job_title",
                    "",
                ),
            ),
        )

        result["company"] = job.get(
            "company",
            "",
        )

        result["location"] = job.get(
            "location",
            "",
        )

        return result

    def match(
        self,
        profile,
        job,
    ):

        return self.match_job(
            profile,
            job,
        )

    def score(
        self,
        profile,
        job,
    ):

        result = self.match_job(
            profile,
            job,
        )

        return result.get(
            "match_score",
            0,
        )

    def rank_jobs(
        self,
        profile,
        jobs,
    ):

        results = []

        if not isinstance(
            jobs,
            list,
        ):

            return results

        for job in jobs:

            if not isinstance(
                job,
                dict,
            ):

                continue

            result = self.match_job(
                profile,
                job,
            )

            result["job"] = job

            results.append(
                result
            )

        results.sort(
            key=lambda item: float(
                item.get(
                    "match_score",
                    0,
                )
                or 0
            ),
            reverse=True,
        )

        return results

    def top_matches(
        self,
        profile,
        jobs,
        limit=10,
    ):

        results = self.rank_jobs(
            profile,
            jobs,
        )

        return results[
            :limit
        ]
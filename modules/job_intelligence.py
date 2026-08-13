from datetime import datetime


class JobIntelligence:

    @staticmethod
    def clean_text(value):

        if value is None:
            return ""

        return str(value).strip()


    @staticmethod
    def normalize_country(value):

        value = JobIntelligence.clean_text(
            value
        )

        country_map = {

            "IN": "India",
            "IND": "India",

            "SG": "Singapore",
            "SGP": "Singapore",

            "AE": "UAE",
            "ARE": "UAE",
            "UAE": "UAE",

            "DE": "Germany",
            "DEU": "Germany",

            "MY": "Malaysia",
            "MYS": "Malaysia",

            "SA": "Saudi Arabia",
            "SAU": "Saudi Arabia",

            "QA": "Qatar",
            "QAT": "Qatar",

            "GB": "United Kingdom",
            "UK": "United Kingdom",

            "CA": "Canada",
            "CAN": "Canada",

            "AU": "Australia",
            "AUS": "Australia",

            "NZ": "New Zealand",
            "NZL": "New Zealand",

            "PL": "Poland",
            "POL": "Poland",

            "FI": "Finland",
            "FIN": "Finland",

            "EE": "Estonia",
            "EST": "Estonia",

            "RO": "Romania",
            "ROU": "Romania",

        }

        return country_map.get(
            value.upper(),
            value,
        )


    @staticmethod
    def has_apply_link(job):

        url = JobIntelligence.clean_text(
            job.get(
                "apply_link",
                ""
            )
        )

        return (
            url.startswith("http://")
            or
            url.startswith("https://")
        )


    @staticmethod
    def is_remote(job):

        values = [

            job.get(
                "remote_friendly",
                False
            ),

            job.get(
                "remote",
                False
            ),

            job.get(
                "work_mode",
                ""
            ),

            job.get(
                "location",
                ""
            ),

        ]

        text = " ".join(
            JobIntelligence.clean_text(
                value
            )
            for value in values
        ).lower()

        return any(
            keyword in text
            for keyword in [
                "remote",
                "work from home",
                "wfh",
                "remote-friendly",
            ]
        )


    @staticmethod
    def has_visa_sponsorship(job):

        value = job.get(
            "visa_sponsorship",
            False
        )

        if isinstance(
            value,
            bool
        ):

            return value

        text = JobIntelligence.clean_text(
            value
        ).lower()

        return text in [
            "true",
            "yes",
            "available",
            "sponsored",
            "sponsorship",
        ]


    @staticmethod
    def score(job):

        try:

            score = float(
                job.get(
                    "executive_score",
                    job.get(
                        "jobhunter_score",
                        0
                    )
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            score = 0


        # Small quality bonuses

        if JobIntelligence.has_apply_link(
            job
        ):

            score += 5


        if JobIntelligence.has_visa_sponsorship(
            job
        ):

            score += 3


        if JobIntelligence.is_remote(
            job
        ):

            score += 1


        return round(
            min(score, 100),
            2,
        )


    @staticmethod
    def deduplicate(jobs):

        unique = {}

        for job in jobs:

            title = JobIntelligence.clean_text(
                job.get(
                    "title",
                    job.get(
                        "role",
                        ""
                    )
                )
            ).lower()

            company = JobIntelligence.clean_text(
                job.get(
                    "company",
                    ""
                )
            ).lower()

            location = JobIntelligence.clean_text(
                job.get(
                    "location",
                    ""
                )
            ).lower()

            key = (
                title,
                company,
                location,
            )

            if key not in unique:

                unique[key] = job

        return list(
            unique.values()
        )


    @staticmethod
    def enrich(jobs):

        enriched = []

        for job in jobs:

            item = dict(job)

            item["country"] = (
                JobIntelligence
                .normalize_country(
                    item.get(
                        "country",
                        ""
                    )
                )
            )

            item["is_remote"] = (
                JobIntelligence.is_remote(
                    item
                )
            )

            item["has_visa"] = (
                JobIntelligence
                .has_visa_sponsorship(
                    item
                )
            )

            item["has_apply_link"] = (
                JobIntelligence
                .has_apply_link(
                    item
                )
            )

            item["intelligence_score"] = (
                JobIntelligence.score(
                    item
                )
            )

            enriched.append(
                item
            )

        return enriched


    @staticmethod
    def filter_jobs(
        jobs,
        country="All",
        remote_only=False,
        visa_only=False,
        apply_only=False,
        minimum_score=0,
    ):

        result = []

        for job in jobs:

            if (
                country != "All"
                and job.get(
                    "country",
                    ""
                ) != country
            ):

                continue


            if (
                remote_only
                and not job.get(
                    "is_remote",
                    False
                )
            ):

                continue


            if (
                visa_only
                and not job.get(
                    "has_visa",
                    False
                )
            ):

                continue


            if (
                apply_only
                and not job.get(
                    "has_apply_link",
                    False
                )
            ):

                continue


            try:

                score = float(
                    job.get(
                        "intelligence_score",
                        0
                    )
                )

            except (
                TypeError,
                ValueError,
            ):

                score = 0


            if score < minimum_score:

                continue


            result.append(
                job
            )

        return result


    @staticmethod
    def sort_jobs(
        jobs,
        sort_by="Best Match",
    ):

        if sort_by == "Newest":

            return sorted(
                jobs,
                key=lambda job:
                    job.get(
                        "posted_date",
                        ""
                    ),
                reverse=True,
            )


        if sort_by == "Company":

            return sorted(
                jobs,
                key=lambda job:
                    JobIntelligence
                    .clean_text(
                        job.get(
                            "company",
                            ""
                        )
                    ).lower(),
            )


        if sort_by == "Salary":

            return sorted(
                jobs,
                key=lambda job:
                    JobIntelligence
                    .clean_text(
                        job.get(
                            "salary",
                            ""
                        )
                    ),
                reverse=True,
            )


        return sorted(
            jobs,
            key=lambda job:
                float(
                    job.get(
                        "intelligence_score",
                        0
                    )
                ),
            reverse=True,
        )


    @staticmethod
    def analyze(
        jobs
    ):

        countries = sorted(
            {
                job.get(
                    "country",
                    ""
                )
                for job in jobs
                if job.get(
                    "country",
                    ""
                )
            }
        )


        return {

            "total_jobs":
                len(jobs),

            "with_apply_link":
                sum(
                    1
                    for job in jobs
                    if job.get(
                        "has_apply_link",
                        False
                    )
                ),

            "visa_jobs":
                sum(
                    1
                    for job in jobs
                    if job.get(
                        "has_visa",
                        False
                    )
                ),

            "remote_jobs":
                sum(
                    1
                    for job in jobs
                    if job.get(
                        "is_remote",
                        False
                    )
                ),

            "countries":
                countries,

        }
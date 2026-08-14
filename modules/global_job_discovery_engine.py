import os
import time

import requests
from dotenv import load_dotenv

from modules.job_freshness_engine import JobFreshnessEngine


load_dotenv()


class GlobalJobDiscoveryEngine:

    # --------------------------------------------------
    # PHASE 7 COUNTRY MAP
    # --------------------------------------------------

    COUNTRIES = {
        "India": "in",
        "Singapore": "sg",
        "United Kingdom": "gb",
        "Germany": "de",
        "United States": "us",
        "Australia": "au",
        "Poland": "pl",
        "Netherlands": "nl",
        "New Zealand": "nz",
        "Romania": "ro",
        "Austria": "at",
        "Greece": "gr",
        "United Arab Emirates": "ae",
    }

    def __init__(
        self,
        app_id=None,
        app_key=None,
    ):

        self.app_id = (
            app_id
            or os.getenv("ADZUNA_APP_ID")
        )

        self.app_key = (
            app_key
            or os.getenv("ADZUNA_APP_KEY")
        )

        self.base_url = (
            "https://api.adzuna.com/v1/api/jobs"
        )

    # ==================================================
    # SEARCH ONE COUNTRY / ONE PAGE
    # ==================================================

    def _search_page(
        self,
        role,
        country_code,
        page,
        results_per_page=25,
    ):

        if not self.app_id or not self.app_key:

            print(
                "Adzuna credentials not configured."
            )

            return []

        url = (
            f"{self.base_url}/"
            f"{country_code}/search/{page}"
        )

        params = {

            "app_id":
                self.app_id,

            "app_key":
                self.app_key,

            "results_per_page":
                results_per_page,

            "what":
                role,

            "content-type":
                "application/json",
        }

        try:

            response = requests.get(
                url,
                params=params,
                timeout=15,
            )

            if response.status_code == 429:

                print(
                    f"Rate limit for {country_code}, "
                    f"page {page}. Waiting..."
                )

                time.sleep(5)

                response = requests.get(
                    url,
                    params=params,
                    timeout=15,
                )

            response.raise_for_status()

            data = response.json()

        except requests.exceptions.RequestException as error:

            print(
                f"Adzuna request failed "
                f"{country_code} page {page}: {error}"
            )

            return []

        jobs = []

        for item in data.get(
            "results",
            [],
        ):

            salary_min = item.get(
                "salary_min"
            )

            salary_max = item.get(
                "salary_max"
            )

            if salary_min and salary_max:

                salary = (
                    f"{salary_min} - {salary_max}"
                )

            elif salary_min:

                salary = (
                    f"{salary_min}+"
                )

            elif salary_max:

                salary = (
                    f"Up to {salary_max}"
                )

            else:

                salary = "Not Disclosed"

            jobs.append(
                {
                    "role":
                        item.get(
                            "title",
                            "",
                        ),

                    "company":
                        item.get(
                            "company",
                            {}
                        ).get(
                            "display_name",
                            "Unknown",
                        ),

                    "country":
                        country_code.upper(),

                    "location":
                        item.get(
                            "location",
                            {}
                        ).get(
                            "display_name",
                            "",
                        ),

                    "salary":
                        salary,

                    "salary_min":
                        salary_min,

                    "salary_max":
                        salary_max,

                    "description":
                        item.get(
                            "description",
                            "",
                        ),

                    "apply_link":
                        item.get(
                            "redirect_url",
                            "",
                        ),

                    "source":
                        "Adzuna",

                    "visa_sponsorship":
                        False,

                    "remote_friendly":
                        False,

                    "posted_date":
                        item.get(
                            "created",
                            "",
                        ),

                    "employment_type":
                        "",

                    "experience_level":
                        "",

                    "executive_score":
                        0.0,

                    "priority_score":
                        0.0,

                    "jobhunter_score":
                        0.0,

                }
            )

        return jobs

    # ==================================================
    # SEARCH ONE COUNTRY
    # ==================================================

    def search_country(
        self,
        role,
        country,
        pages=3,
        results_per_page=25,
        delay=0.25,
    ):

        country_code = self.COUNTRIES.get(
            country
        )

        if not country_code:

            print(
                f"Unknown country: {country}"
            )

            return []

        country_jobs = []

        for page in range(
            1,
            pages + 1,
        ):

            results = self._search_page(
                role=role,
                country_code=country_code,
                page=page,
                results_per_page=results_per_page,
            )

            if not results:

                break

            country_jobs.extend(
                results
            )

            print(
                f"{country}: page {page} "
                f"→ {len(results)} jobs"
            )

            time.sleep(
                delay
            )

        return country_jobs

    # ==================================================
    # SEARCH GLOBALLY
    # ==================================================

    def search(
        self,
        role,
        countries=None,
        pages=3,
        results_per_page=25,
        freshness_hours=None,
    ):

        role = str(
            role or ""
        ).strip()

        if not role:

            return []

        if countries is None:

            countries = list(
                self.COUNTRIES.keys()
            )

        all_jobs = []

        print(
            f"\nGlobal discovery: {role}"
        )

        print(
            f"Countries: {len(countries)}"
        )

        print(
            f"Pages per country: {pages}"
        )

        for country in countries:

            jobs = self.search_country(
                role=role,
                country=country,
                pages=pages,
                results_per_page=results_per_page,
            )

            all_jobs.extend(
                jobs
            )

            print(
                f"✓ {country}: "
                f"{len(jobs)} jobs"
            )

        print(
            f"Raw global jobs: {len(all_jobs)}"
        )

        unique_jobs = (
            self.deduplicate(
                all_jobs
            )
        )

        print(
            f"Unique global jobs: "
            f"{len(unique_jobs)}"
        )

        # --------------------------------------------------
        # FRESHNESS
        # --------------------------------------------------

        unique_jobs = (
            JobFreshnessEngine
            .analyze_jobs(
                unique_jobs
            )
        )

        # --------------------------------------------------
        # OPTIONAL FRESHNESS FILTER
        # --------------------------------------------------

        if freshness_hours is not None:

            unique_jobs = [

                job

                for job in unique_jobs

                if (
                    job.get(
                        "age_hours"
                    ) is not None

                    and

                    job.get(
                        "age_hours"
                    ) <= freshness_hours
                )

            ]

            print(
                f"Jobs within "
                f"{freshness_hours} hours: "
                f"{len(unique_jobs)}"
            )

        # --------------------------------------------------
        # SORT
        # --------------------------------------------------

        unique_jobs.sort(
            key=lambda job: (
                job.get(
                    "freshness_priority",
                    99,
                ),
                job.get(
                    "age_hours",
                    float("inf"),
                ),
            )
        )

        return unique_jobs

    # ==================================================
    # DEDUPLICATE
    # ==================================================

    @staticmethod
    def deduplicate(
        jobs
    ):

        unique = {}

        for job in jobs:

            role = str(
                job.get(
                    "role",
                    job.get(
                        "title",
                        "",
                    ),
                )
            ).strip().lower()

            company = str(
                job.get(
                    "company",
                    "",
                )
            ).strip().lower()

            location = str(
                job.get(
                    "location",
                    "",
                )
            ).strip().lower()

            apply_link = str(
                job.get(
                    "apply_link",
                    "",
                )
            ).strip().lower()

            # Prefer URL when available
            if apply_link:

                key = (
                    company,
                    role,
                    apply_link,
                )

            else:

                key = (
                    company,
                    role,
                    location,
                )

            if key not in unique:

                unique[key] = job

        return list(
            unique.values()
        )

    # ==================================================
    # FRESHNESS SUMMARY
    # ==================================================

    def freshness_summary(
        self,
        jobs,
    ):

        return (
            JobFreshnessEngine.summary(
                jobs
            )
        )


# ======================================================
# DIRECT TEST
# ======================================================

if __name__ == "__main__":

    engine = (
        GlobalJobDiscoveryEngine()
    )

    jobs = engine.search(
        role="Head of Sales",
        countries=[
            "India",
            "Singapore",
            "Germany",
            "Australia",
            "Romania",
            "Austria",
            "Greece",
        ],
        pages=2,
        results_per_page=20,
    )

    print()
    print(
        "GLOBAL JOBS:",
        len(jobs),
    )

    print()
    print(
        "FRESHNESS SUMMARY:"
    )

    print(
        engine.freshness_summary(
            jobs
        )
    )

    print()
    print(
        "TOP 20:"
    )

    for index, job in enumerate(
        jobs[:20],
        start=1,
    ):

        print(
            index,
            "|",
            job.get(
                "role",
                "",
            ),
            "|",
            job.get(
                "company",
                "",
            ),
            "|",
            job.get(
                "country",
                "",
            ),
            "|",
            job.get(
                "freshness_bucket",
                "",
            ),
            "|",
            job.get(
                "age_hours",
                "",
            ),
            "hrs",
        )
import re
from urllib.parse import urlparse

from modules.job_enrichment_engine import (
    JobEnrichmentEngine,
)
from modules.live_company_intelligence import (
    LiveCompanyIntelligence,
)


class GlobalJobEnrichmentEngine:

    def __init__(self):

        self.company_intelligence = (
            LiveCompanyIntelligence()
        )

    # ==========================================================
    # TEXT NORMALIZATION
    # ==========================================================

    @staticmethod
    def _normalize_company_name(
        company,
    ):

        text = str(
            company or ""
        ).lower().strip()

        # Remove common company suffixes
        text = re.sub(
            r"\b(private limited|pvt ltd|pvt\. ltd|"
            r"limited|ltd|llp|incorporated|inc|corp|"
            r"corporation|co|company|gmbh|pte ltd|"
            r"pty ltd|plc|s\.a\.|sarl)\b",
            " ",
            text,
        )

        text = re.sub(
            r"[^a-z0-9]+",
            " ",
            text,
        )

        return [
            token
            for token in text.split()
            if len(token) >= 3
        ]

    # ==========================================================
    # WEBSITE VALIDATION
    # ==========================================================

    @classmethod
    def validate_company_website(
        cls,
        company,
        website,
    ):

        if not website:

            return {
                "website":
                    "Not available",

                "verified":
                    False,

                "verification":
                    "Unavailable",
            }

        website = str(
            website
        ).strip()

        if not website:

            return {
                "website":
                    "Not available",

                "verified":
                    False,

                "verification":
                    "Unavailable",
            }

        try:

            parsed = urlparse(
                website
            )

            domain = (
                parsed.netloc
                or parsed.path
                or ""
            ).lower()

            domain = domain.split(
                ":"
            )[0]

            domain_tokens = re.findall(
                r"[a-z0-9]+",
                domain,
            )

        except Exception:

            return {
                "website":
                    "Not available",

                "verified":
                    False,

                "verification":
                    "Invalid URL",
            }

        company_tokens = (
            cls._normalize_company_name(
                company
            )
        )

        # ------------------------------------------------------
        # Strong verification:
        # At least one meaningful company token
        # appears in the domain.
        # ------------------------------------------------------

        matched_tokens = [

            token

            for token in company_tokens

            if token in domain_tokens
            or any(
                token in domain_token
                for domain_token in domain_tokens
            )
        ]

        if matched_tokens:

            return {
                "website":
                    website,

                "verified":
                    True,

                "verification":
                    "Domain matched company name",
            }

        # ------------------------------------------------------
        # Do not present unrelated domains as verified.
        # ------------------------------------------------------

        return {
            "website":
                "Not verified",

            "verified":
                False,

            "verification":
                "Company-domain match could not be confirmed",
        }

    # ==========================================================
    # ENRICH ONE JOB
    # ==========================================================

    def enrich(
        self,
        job,
    ):

        enriched = dict(
            job
        )

        # ------------------------------------------------------
        # Existing company lookup
        # ------------------------------------------------------

        candidate_website = ""

        try:

            candidate_website = (
                self.company_intelligence
                .find_company_website(
                    enriched.get(
                        "company",
                        "",
                    )
                )
            )

        except Exception as error:

            enriched[
                "company_intelligence_error"
            ] = str(error)

        # ------------------------------------------------------
        # Validate company website
        # ------------------------------------------------------

        website_check = (
            self.validate_company_website(
                enriched.get(
                    "company",
                    "",
                ),
                candidate_website,
            )
        )

        if website_check["verified"]:

            enriched[
                "company_website"
            ] = website_check["website"]

            website = website_check[
                "website"
            ].rstrip("/")

            enriched[
                "careers_page"
            ] = (
                website
                + "/careers"
            )

            enriched[
                "contact_page"
            ] = (
                website
                + "/contact"
            )

            enriched[
                "linkedin_company"
            ] = (
                "https://www.linkedin.com/search/results/companies/?keywords="
                + str(
                    enriched.get(
                        "company",
                        "",
                    )
                ).replace(
                    " ",
                    "%20",
                )
            )

        else:

            enriched[
                "company_website"
            ] = "Not verified"

            enriched[
                "careers_page"
            ] = "Not available"

            enriched[
                "contact_page"
            ] = "Not available"

            enriched[
                "linkedin_company"
            ] = (
                "https://www.linkedin.com/search/results/companies/?keywords="
                + str(
                    enriched.get(
                        "company",
                        "",
                    )
                ).replace(
                    " ",
                    "%20",
                )
            )

        enriched[
            "website_verified"
        ] = website_check[
            "verified"
        ]

        enriched[
            "website_verification"
        ] = website_check[
            "verification"
        ]

        # ------------------------------------------------------
        # Standard enrichment
        # ------------------------------------------------------

        enriched = (
            JobEnrichmentEngine.enrich(
                enriched
            )
        )

        # Preserve the validated website state
        enriched[
            "company_website"
        ] = (
            "Not verified"
            if not website_check[
                "verified"
            ]
            else website_check[
                "website"
            ]
        )

        enriched[
            "company_website_verified"
        ] = (
            website_check[
                "verified"
            ]
        )

        # ------------------------------------------------------
        # Sources
        # ------------------------------------------------------

        sources = []

        if enriched.get(
            "source"
        ):

            sources.append(
                enriched[
                    "source"
                ]
            )

        if enriched.get(
            "company_website_verified",
            False,
        ):

            sources.append(
                "Company Website"
            )

        if enriched.get(
            "salary_available",
            False,
        ):

            sources.append(
                "Job Posting Salary"
            )

        enriched[
            "enrichment_sources"
        ] = sources

        # ------------------------------------------------------
        # Recruiter / HR contact
        # ------------------------------------------------------

        enriched[
            "recruiter_contact_available"
        ] = (
            enriched.get(
                "contact_status"
            )
            == "Available"
        )

        # ------------------------------------------------------
        # Data completeness
        # ------------------------------------------------------

        enriched[
            "data_completeness"
        ] = (
            JobEnrichmentEngine
            .completeness_score(
                enriched
            )
        )

        return enriched

    # ==========================================================
    # ENRICH MANY JOBS
    # ==========================================================

    def enrich_jobs(
        self,
        jobs,
    ):

        return [
            self.enrich(job)
            for job in (
                jobs or []
            )
        ]


# ==========================================================
# DIRECT TEST
# ==========================================================

if __name__ == "__main__":

    engine = (
        GlobalJobEnrichmentEngine()
    )

    samples = [

        {
            "role":
                "Head of Sales",

            "company":
                "Microsoft",

            "country":
                "US",

            "salary":
                "Not Disclosed",

            "source":
                "Adzuna",

            "apply_link":
                "https://example.com/job",
        },

        {
            "role":
                "Head of Sales",

            "company":
                "Example Technologies",

            "country":
                "SG",

            "salary":
                "SGD 160000 - 190000",

            "salary_min":
                160000,

            "salary_max":
                190000,

            "source":
                "Adzuna",

            "apply_link":
                "https://example.com/job",
        },

    ]

    results = (
        engine.enrich_jobs(
            samples
        )
    )

    print(
        "GLOBAL ENRICHMENT TEST"
    )

    for result in results:

        print()
        print(
            "Company:",
            result.get(
                "company"
            )
        )

        print(
            "Website:",
            result.get(
                "company_website"
            )
        )

        print(
            "Website verified:",
            result.get(
                "company_website_verified"
            )
        )

        print(
            "Verification:",
            result.get(
                "website_verification"
            )
        )

        print(
            "Salary:",
            result.get(
                "salary"
            )
        )

        print(
            "Currency:",
            result.get(
                "currency"
            )
        )

        print(
            "Recruiter:",
            result.get(
                "recruiter_name"
            )
        )

        print(
            "Completeness:",
            result.get(
                "data_completeness"
            ),
            "%"
        )

        print(
            "Flags:",
            result.get(
                "verification_flags"
            )
        )
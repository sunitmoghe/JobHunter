import re
from urllib.parse import urlparse


class JobEnrichmentEngine:

    """
    Phase 7E enrichment layer.

    This module does NOT modify the existing job engines.
    It combines information already present in a job record,
    plus safe derived metadata and existing company/salary
    intelligence where available.

    Missing information is explicitly represented as
    'Not available' instead of being invented.
    """

    COUNTRY_CURRENCIES = {
        "SG": "SGD",
        "IN": "INR",
        "DE": "EUR",
        "AU": "AUD",
        "AT": "EUR",
        "RO": "RON",
        "GR": "EUR",
        "GB": "GBP",
        "US": "USD",
        "NZ": "NZD",
        "PL": "PLN",
        "NL": "EUR",
        "AE": "AED",
        "MY": "MYR",
        "SA": "SAR",
        "CA": "CAD",
    }

    # ----------------------------------------------------------
    # NORMALIZATION
    # ----------------------------------------------------------

    @staticmethod
    def _text(value, default="Not available"):

        if value is None:
            return default

        value = str(value).strip()

        return value if value else default

    # ----------------------------------------------------------
    # COMPANY WEBSITE
    # ----------------------------------------------------------

    @staticmethod
    def extract_company_domain(job):

        candidates = [
            job.get("company_url"),
            job.get("company_website"),
            job.get("website"),
        ]

        for value in candidates:

            if value:

                value = str(value).strip()

                if value:

                    parsed = urlparse(
                        value
                    )

                    if parsed.netloc:
                        return parsed.netloc

                    return value

        return "Not available"

    # ----------------------------------------------------------
    # SALARY
    # ----------------------------------------------------------

    @classmethod
    def salary_details(cls, job):

        salary = cls._text(
            job.get("salary"),
            "Not disclosed",
        )

        salary_min = job.get(
            "salary_min"
        )

        salary_max = job.get(
            "salary_max"
        )

        country = cls._text(
            job.get("country"),
            "",
        ).upper()

        currency = (
            job.get("currency")
            or cls.COUNTRY_CURRENCIES.get(
                country,
                "USD",
            )
        )

        if (
            salary_min is not None
            or salary_max is not None
        ):

            return {
                "salary":
                    salary,

                "salary_min":
                    salary_min,

                "salary_max":
                    salary_max,

                "currency":
                    currency,

                "salary_source":
                    "Job posting",

                "salary_available":
                    True,
            }

        return {
            "salary":
                salary,

            "salary_min":
                None,

            "salary_max":
                None,

            "currency":
                currency,

            "salary_source":
                "Not available",

            "salary_available":
                False,
        }

    # ----------------------------------------------------------
    # CONTACT DETAILS
    # ----------------------------------------------------------

    @staticmethod
    def contact_details(job):

        recruiter_name = (
            job.get("recruiter_name")
            or job.get("recruiter")
            or job.get("contact_name")
        )

        recruiter_email = (
            job.get("recruiter_email")
            or job.get("contact_email")
            or job.get("hr_email")
        )

        recruiter_phone = (
            job.get("recruiter_phone")
            or job.get("contact_phone")
            or job.get("hr_phone")
        )

        recruiter_linkedin = (
            job.get("recruiter_linkedin")
            or job.get("linkedin")
        )

        return {

            "recruiter_name":
                JobEnrichmentEngine._text(
                    recruiter_name
                ),

            "recruiter_email":
                JobEnrichmentEngine._text(
                    recruiter_email
                ),

            "recruiter_phone":
                JobEnrichmentEngine._text(
                    recruiter_phone
                ),

            "recruiter_linkedin":
                JobEnrichmentEngine._text(
                    recruiter_linkedin
                ),

            "contact_status":
                (
                    "Available"
                    if any(
                        value
                        for value in [
                            recruiter_name,
                            recruiter_email,
                            recruiter_phone,
                            recruiter_linkedin,
                        ]
                    )
                    else "Not available"
                ),
        }

    # ----------------------------------------------------------
    # APPLICATION URL
    # ----------------------------------------------------------

    @staticmethod
    def application_details(job):

        apply_link = (
            job.get("apply_link")
            or job.get("redirect_url")
            or job.get("url")
            or job.get("link")
        )

        apply_link = (
            JobEnrichmentEngine._text(
                apply_link
            )
        )

        source = JobEnrichmentEngine._text(
            job.get("source"),
            "Unknown",
        )

        return {

            "apply_link":
                apply_link,

            "application_available":
                apply_link != "Not available",

            "application_source":
                source,
        }

    # ----------------------------------------------------------
    # COMPANY INFORMATION
    # ----------------------------------------------------------

    @staticmethod
    def company_details(job):

        company = JobEnrichmentEngine._text(
            job.get("company"),
            "Unknown Company",
        )

        industry = (
            job.get("industry")
            or "Not available"
        )

        employees = (
            job.get("employee_count")
            or "Not available"
        )

        headquarters = (
            job.get("headquarters")
            or "Not available"
        )

        verified = job.get(
            "verified_company"
        )

        if verified is None:

            verification = "Unknown"

        elif verified:

            verification = "Verified"

        else:

            verification = "Unverified"

        company_website = (
            job.get("company_url")
            or job.get("company_website")
            or job.get("website")
        )

        return {

            "company":
                company,

            "company_website":
                JobEnrichmentEngine._text(
                    company_website
                ),

            "company_domain":
                JobEnrichmentEngine.extract_company_domain(
                    job
                ),

            "industry":
                industry,

            "employee_count":
                employees,

            "headquarters":
                headquarters,

            "company_rating":
                job.get(
                    "company_rating",
                    "Not available",
                ),

            "growth_score":
                job.get(
                    "growth_score",
                    "Not available",
                ),

            "layoff_risk":
                job.get(
                    "layoff_risk",
                    "Not available",
                ),

            "company_verification":
                verification,
        }

    # ----------------------------------------------------------
    # JOB METADATA
    # ----------------------------------------------------------

    @staticmethod
    def job_details(job):

        role = (
            job.get("role")
            or job.get("title")
            or "Executive Position"
        )

        country = JobEnrichmentEngine._text(
            job.get("country"),
            "Unknown",
        )

        location = JobEnrichmentEngine._text(
            job.get("location"),
            "Not available",
        )

        employment_type = JobEnrichmentEngine._text(
            job.get("employment_type"),
            "Not available",
        )

        experience_level = JobEnrichmentEngine._text(
            job.get("experience_level"),
            "Not available",
        )

        return {

            "role":
                str(role).strip(),

            "country":
                country,

            "location":
                location,

            "employment_type":
                employment_type,

            "experience_level":
                experience_level,

            "posted_date":
                JobEnrichmentEngine._text(
                    job.get("posted_date"),
                    "Not available",
                ),

            "source":
                JobEnrichmentEngine._text(
                    job.get("source"),
                    "Unknown",
                ),

            "description":
                JobEnrichmentEngine._text(
                    job.get("description"),
                    "Not available",
                ),
        }

    # ----------------------------------------------------------
    # VERIFY DATA QUALITY
    # ----------------------------------------------------------

    @staticmethod
    def verification_flags(job):

        flags = []

        if (
            not job.get("company")
            or str(
                job.get("company")
            ).strip() == ""
        ):

            flags.append(
                "Company name unavailable"
            )

        if not (
            job.get("apply_link")
            or job.get("url")
            or job.get("link")
        ):

            flags.append(
                "Application URL unavailable"
            )

        if not (
            job.get("salary")
            or job.get("salary_min") is not None
            or job.get("salary_max") is not None
        ):

            flags.append(
                "Salary not disclosed"
            )

        if not (
            job.get("recruiter_name")
            or job.get("recruiter_email")
            or job.get("hr_email")
            or job.get("recruiter_linkedin")
        ):

            flags.append(
                "Recruiter/HR contact unavailable"
            )

        return flags

    # ----------------------------------------------------------
    # ENRICH ONE JOB
    # ----------------------------------------------------------

    @classmethod
    def enrich(cls, job):

        enriched = dict(job)

        enriched.update(
            cls.job_details(job)
        )

        enriched.update(
            cls.company_details(job)
        )

        enriched.update(
            cls.salary_details(job)
        )

        enriched.update(
            cls.contact_details(job)
        )

        enriched.update(
            cls.application_details(job)
        )

        flags = cls.verification_flags(
            job
        )

        enriched[
            "verification_flags"
        ] = flags

        enriched[
            "data_completeness"
        ] = cls.completeness_score(
            enriched
        )

        return enriched

    # ----------------------------------------------------------
    # ENRICH MANY JOBS
    # ----------------------------------------------------------

    @classmethod
    def enrich_jobs(cls, jobs):

        return [
            cls.enrich(job)
            for job in (
                jobs or []
            )
        ]

    # ----------------------------------------------------------
    # COMPLETENESS
    # ----------------------------------------------------------

    @staticmethod
    def completeness_score(job):

        fields = [

            job.get("company"),

            job.get("role"),

            job.get("country"),

            job.get("location"),

            job.get("apply_link"),

            job.get("salary"),

            job.get("company_website"),

            job.get("recruiter_name"),

            job.get("recruiter_email"),

            job.get("recruiter_linkedin"),

        ]

        available = 0

        for value in fields:

            if value is None:
                continue

            text = str(
                value
            ).strip()

            if (
                text
                and text.lower()
                not in {
                    "not available",
                    "not disclosed",
                    "unknown",
                }
            ):

                available += 1

        return round(
            (
                available
                / len(fields)
            ) * 100,
            2,
        )


# ==========================================================
# DIRECT TEST
# ==========================================================

if __name__ == "__main__":

    sample_job = {

        "role":
            "Head of Sales",

        "company":
            "Example Technologies",

        "country":
            "SG",

        "location":
            "Singapore",

        "salary":
            "SGD 160,000 - 190,000",

        "salary_min":
            160000,

        "salary_max":
            190000,

        "apply_link":
            "https://example.com/jobs/head-sales",

        "source":
            "Example Careers",

        "posted_date":
            "2026-08-14T08:00:00Z",

    }

    result = (
        JobEnrichmentEngine.enrich(
            sample_job
        )
    )

    print(
        "ENRICHMENT TEST"
    )

    print(
        "Company:",
        result["company"],
    )

    print(
        "Website:",
        result["company_website"],
    )

    print(
        "Salary:",
        result["salary"],
    )

    print(
        "Currency:",
        result["currency"],
    )

    print(
        "Recruiter:",
        result["recruiter_name"],
    )

    print(
        "Application:",
        result["apply_link"],
    )

    print(
        "Completeness:",
        result["data_completeness"],
        "%",
    )

    print(
        "Verification flags:",
        result["verification_flags"],
    )
from modules.resume_library_engine import ResumeLibraryEngine
from modules.resume_parser import ResumeParser
from modules.ats_matcher import ATSMatcher


class MultiResumeMatcher:

    def __init__(self):

        self.library = (
            ResumeLibraryEngine()
        )

    # ==========================================================
    # MATCH ONE RESUME
    # ==========================================================

    def match_resume(
        self,
        resume,
        job_description,
    ):

        resume_path = resume.get(
            "file_path",
            "",
        )

        if not resume_path:

            return {
                "resume_id":
                    resume.get(
                        "resume_id",
                        "",
                    ),

                "resume_name":
                    resume.get(
                        "resume_name",
                        "Resume",
                    ),

                "score": 0,

                "error":
                    "Resume file path unavailable.",
            }

        try:

            parser = ResumeParser(
                resume_path
            )

            resume_text = (
                parser.read_resume()
            )

        except Exception as error:

            return {
                "resume_id":
                    resume.get(
                        "resume_id",
                        "",
                    ),

                "resume_name":
                    resume.get(
                        "resume_name",
                        "Resume",
                    ),

                "score": 0,

                "error":
                    str(error),
            }

        matcher = ATSMatcher(
            resume_text,
            job_description,
        )

        result = (
            matcher.calculate_match()
        )

        return {

            "resume_id":
                resume.get(
                    "resume_id",
                    "",
                ),

            "resume_name":
                resume.get(
                    "resume_name",
                    "Resume",
                ),

            "original_filename":
                resume.get(
                    "original_filename",
                    "",
                ),

            "target_roles":
                resume.get(
                    "target_roles",
                    [],
                ),

            "target_countries":
                resume.get(
                    "target_countries",
                    [],
                ),

            "score":
                result.get(
                    "score",
                    0,
                ),

            "matched":
                result.get(
                    "matched",
                    [],
                ),

            "missing":
                result.get(
                    "missing",
                    [],
                ),

            "matched_count":
                result.get(
                    "matched_count",
                    0,
                ),

            "missing_count":
                result.get(
                    "missing_count",
                    0,
                ),

            "interview_probability":
                result.get(
                    "interview_probability",
                    0,
                ),

            "dynamic_missing_keywords":
                result.get(
                    "dynamic_missing_keywords",
                    [],
                ),

            "recommendations":
                result.get(
                    "recommendations",
                    [],
                ),

            "error":
                None,
        }

    # ==========================================================
    # MATCH ALL ACTIVE RESUMES
    # ==========================================================

    def match_all(
        self,
        job_description,
    ):

        resumes = (
            self.library
            .get_all_resumes(
                include_archived=False
            )
        )

        results = []

        for resume in resumes:

            # Current ResumeParser supports PDF/DOCX.
            # Skip unsupported formats cleanly.
            file_type = str(
                resume.get(
                    "format",
                    "",
                )
            ).upper()

            if file_type not in {
                "PDF",
                "DOCX",
            }:

                results.append({
                    "resume_id":
                        resume.get(
                            "resume_id",
                            "",
                        ),

                    "resume_name":
                        resume.get(
                            "resume_name",
                            "Resume",
                        ),

                    "score": 0,

                    "error":
                        "Unsupported format. "
                        "Use PDF or DOCX.",
                })

                continue

            results.append(
                self.match_resume(
                    resume,
                    job_description,
                )
            )

        results.sort(
            key=lambda item: (
                -float(
                    item.get(
                        "score",
                        0,
                    )
                    or 0
                ),
                -int(
                    item.get(
                        "matched_count",
                        0,
                    )
                    or 0
                ),
            )
        )

        return results

    # ==========================================================
    # BEST RESUME
    # ==========================================================

    def best_resume(
        self,
        job_description,
    ):

        results = self.match_all(
            job_description
        )

        valid_results = [
            result
            for result in results
            if not result.get(
                "error"
            )
        ]

        if not valid_results:

            return None

        return valid_results[0]

    # ==========================================================
    # JOB RESULT
    # ==========================================================

    def analyze_job(
        self,
        job,
    ):

        description = (
            job.get(
                "description",
                job.get(
                    "job_description",
                    "",
                ),
            )
            or ""
        )

        best = self.best_resume(
            description
        )

        all_matches = self.match_all(
            description
        )

        return {

            "job_title":
                job.get(
                    "title",
                    job.get(
                        "role",
                        "",
                    ),
                ),

            "company":
                job.get(
                    "company",
                    "",
                ),

            "best_resume":
                best,

            "all_resume_matches":
                all_matches,

        }


# ==========================================================
# DIRECT TEST
# ==========================================================

if __name__ == "__main__":

    matcher = (
        MultiResumeMatcher()
    )

    resumes = (
        matcher.library
        .get_all_resumes(
            include_archived=False
        )
    )

    print(
        "ACTIVE RESUMES:",
        len(resumes),
    )

    sample_jd = """
    Head of Sales

    We are looking for an executive sales leader
    with strong experience in revenue growth,
    strategic sales leadership, P&L management,
    enterprise customers, forecasting, CRM,
    SaaS and business transformation.

    The candidate should have experience leading
    large teams and growing international markets.
    """

    results = matcher.match_all(
        sample_jd
    )

    print(
        "MATCH RESULTS:",
        len(results),
    )

    for index, result in enumerate(
        results,
        start=1,
    ):

        print(
            index,
            "|",
            result.get(
                "resume_name"
            ),
            "| ATS:",
            result.get(
                "score"
            ),
            "| Matched:",
            result.get(
                "matched_count",
                0,
            ),
            "| Missing:",
            result.get(
                "missing_count",
                0,
            ),
        )

        if result.get(
            "error"
        ):

            print(
                "   ERROR:",
                result[
                    "error"
                ],
            )

    best = matcher.best_resume(
        sample_jd
    )

    if best:

        print()
        print(
            "BEST RESUME:",
            best.get(
                "resume_name"
            ),
            "| ATS:",
            best.get(
                "score"
            ),
        )

    else:

        print(
            "BEST RESUME: None"
        )
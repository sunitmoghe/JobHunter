from modules.unified_job_engine import UnifiedJobEngine
from modules.executive_config import EXECUTIVE_ROLES
from modules.executive_scoring_engine import ExecutiveScoringEngine
from modules.parallel_search_engine import ParallelSearchEngine
from modules.job_cache import JobCache
from modules.job_normalizer import JobNormalizer
from modules.job_intelligence import JobIntelligence


class ExecutiveAIAgent:

    def __init__(self):

        self.engine = UnifiedJobEngine()

        self.parallel_engine = ParallelSearchEngine(
            self.engine
        )

        self.scoring = ExecutiveScoringEngine()

        self.cache = JobCache()


    # ==================================================
    # PUBLIC SEARCH METHOD
    # ==================================================

    def search_jobs(
        self,
        role=None,
        max_roles=None,
        selected_countries=None,
    ):

        if role:

            return self.search_single_role(
                role
            )

        return self.search_all_roles(
            max_roles=max_roles,
            selected_countries=selected_countries,
        )


    # ==================================================
    # SINGLE ROLE SEARCH
    # ==================================================

    def search_single_role(
        self,
        role,
    ):

        cached_jobs = self.cache.get_jobs(
            role
        )

        if cached_jobs:

            jobs = JobNormalizer.normalize_many(
                cached_jobs
            )

            return JobIntelligence.enrich(
                JobIntelligence.deduplicate(
                    jobs
                )
            )


        jobs = self.engine.search_jobs(
            role
        )

        jobs = JobNormalizer.normalize_many(
            jobs
        )


        if not jobs:

            return []


        processed_jobs = []


        for job in jobs:

            job["executive_role"] = role


            # --------------------------------------------------
            # EXECUTIVE SCORING
            # --------------------------------------------------

            score_data = (
                self.scoring.calculate_score(
                    job
                )
            )


            executive_score = (
                score_data.get(
                    "executive_fit",
                    0,
                )
            )


            job["executive_score"] = (
                executive_score
            )


            job["score_details"] = (
                score_data
            )


            job["priority"] = (
                self.get_priority(
                    executive_score
                )
            )


            job["recommendation"] = (
                self.get_recommendation(
                    executive_score
                )
            )


            processed_jobs.append(
                job
            )


        # --------------------------------------------------
        # JOB INTELLIGENCE
        # --------------------------------------------------

        processed_jobs = (
            JobIntelligence.deduplicate(
                processed_jobs
            )
        )


        processed_jobs = (
            JobIntelligence.enrich(
                processed_jobs
            )
        )


        # --------------------------------------------------
        # SAVE CACHE
        # --------------------------------------------------

        self.cache.save_jobs(
            role,
            processed_jobs
        )


        return processed_jobs


    # ==================================================
    # ALL ROLES SEARCH
    # ==================================================

    def search_all_roles(
        self,
        max_roles=None,
        selected_countries=None,
    ):

        cache_key = (
            "ALL_EXECUTIVE_JOBS"
        )


        cached = self.cache.get_jobs(
            cache_key
        )


        if cached:

            jobs = (
                JobNormalizer.normalize_many(
                    cached
                )
            )


            jobs = (
                JobIntelligence.deduplicate(
                    jobs
                )
            )


            return JobIntelligence.enrich(
                jobs
            )


        if max_roles is None:

            roles = EXECUTIVE_ROLES

        else:

            roles = EXECUTIVE_ROLES[
                :max_roles
            ]


        jobs = (
            self.parallel_engine.search_roles(
                roles,
                selected_countries,
            )
        )


        jobs = JobNormalizer.normalize_many(
            jobs
        )


        if not jobs:

            return []


        executive_jobs = []


        for job in jobs:

            # --------------------------------------------------
            # EXECUTIVE SCORING
            # --------------------------------------------------

            score_data = (
                self.scoring.calculate_score(
                    job
                )
            )


            executive_score = (
                score_data.get(
                    "executive_fit",
                    0,
                )
            )


            job["executive_score"] = (
                executive_score
            )


            job["score_details"] = (
                score_data
            )


            job["priority"] = (
                self.get_priority(
                    executive_score
                )
            )


            job["recommendation"] = (
                self.get_recommendation(
                    executive_score
                )
            )


            executive_jobs.append(
                job
            )


        # --------------------------------------------------
        # REMOVE DUPLICATES
        # --------------------------------------------------

        executive_jobs = (
            JobIntelligence.deduplicate(
                executive_jobs
            )
        )


        # --------------------------------------------------
        # ENRICH JOBS
        # --------------------------------------------------

        executive_jobs = (
            JobIntelligence.enrich(
                executive_jobs
            )
        )


        # --------------------------------------------------
        # SORT BY INTELLIGENCE SCORE
        # --------------------------------------------------

        executive_jobs = sorted(
            executive_jobs,
            key=lambda job:
                float(
                    job.get(
                        "intelligence_score",
                        0,
                    )
                ),
            reverse=True,
        )


        # --------------------------------------------------
        # SAVE CACHE
        # --------------------------------------------------

        self.cache.save_jobs(
            cache_key,
            executive_jobs,
        )


        return executive_jobs


    # ==================================================
    # PRIORITY
    # ==================================================

    def get_priority(
        self,
        score,
    ):

        if score >= 90:

            return "Critical"


        if score >= 80:

            return "High"


        if score >= 70:

            return "Medium"


        return "Low"


    # ==================================================
    # RECOMMENDATION
    # ==================================================

    def get_recommendation(
        self,
        score,
    ):

        if score >= 90:

            return "Strongly Recommended"


        if score >= 80:

            return "Recommended"


        if score >= 70:

            return "Consider"


        return "Low Priority"


    # ==================================================
    # CLEAR CACHE
    # ==================================================

    def clear_cache(
        self,
    ):

        self.cache.clear_cache()
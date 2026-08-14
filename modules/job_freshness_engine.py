from datetime import datetime, timezone


class JobFreshnessEngine:

    BUCKETS = [
        (12, "IMMEDIATE", 1),
        (24, "VERY HIGH", 2),
        (36, "HIGH", 3),
        (48, "PRIORITY", 4),
        (72, "NORMAL", 5),
        (168, "LOWER", 6),
    ]

    # ==========================================================
    # PARSE POSTING DATE
    # ==========================================================

    @staticmethod
    def parse_posted_date(value):

        if value is None:
            return None

        text = str(value).strip()

        if not text:
            return None

        # ISO timestamp ending in Z
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"

        try:

            parsed = datetime.fromisoformat(text)

        except ValueError:

            formats = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d",
                "%d-%m-%Y",
            ]

            parsed = None

            for fmt in formats:

                try:

                    parsed = datetime.strptime(
                        text,
                        fmt,
                    )

                    break

                except ValueError:

                    continue

            if parsed is None:
                return None

        if parsed.tzinfo is None:

            parsed = parsed.replace(
                tzinfo=timezone.utc
            )

        return parsed.astimezone(
            timezone.utc
        )

    # ==========================================================
    # ANALYZE ONE JOB
    # ==========================================================

    @classmethod
    def analyze(
        cls,
        job,
        now=None,
    ):

        item = dict(job)

        posted_value = (
            item.get("posted_date")
            or item.get("published_at")
            or item.get("date")
            or item.get("created")
        )

        posted_dt = cls.parse_posted_date(
            posted_value
        )

        # ------------------------------------------------------
        # NO POSTING DATE
        # ------------------------------------------------------

        if posted_dt is None:

            item["age_hours"] = None
            item["age_minutes"] = None
            item["freshness_bucket"] = "UNKNOWN"
            item["freshness_priority"] = 99
            item["freshness_label"] = (
                "Posting age unavailable"
            )
            item["is_fresh"] = False
            item["future_timestamp"] = False

            return item

        # ------------------------------------------------------
        # CURRENT TIME
        # ------------------------------------------------------

        if now is None:

            now = datetime.now(
                timezone.utc
            )

        elif now.tzinfo is None:

            now = now.replace(
                tzinfo=timezone.utc
            )

        else:

            now = now.astimezone(
                timezone.utc
            )

        # ------------------------------------------------------
        # AGE
        # ------------------------------------------------------

        age_seconds = (
            now - posted_dt
        ).total_seconds()

        future_timestamp = (
            age_seconds < 0
        )

        if future_timestamp:

            age_seconds = 0

        age_minutes = (
            age_seconds / 60
        )

        age_hours = (
            age_seconds / 3600
        )

        # ------------------------------------------------------
        # FRESHNESS BUCKET
        # ------------------------------------------------------

        bucket = "STALE"
        priority = 7

        for max_hours, label, rank in cls.BUCKETS:

            if age_hours <= max_hours:

                bucket = label
                priority = rank

                break

        # ------------------------------------------------------
        # HUMAN LABEL
        # ------------------------------------------------------

        if future_timestamp:

            urgency_label = (
                "🟢 Just posted / timestamp ahead of search clock"
            )

        elif age_hours <= 12:

            urgency_label = (
                "🚨 Posted within 12 hours"
            )

        elif age_hours <= 24:

            urgency_label = (
                "🔥 Posted within 24 hours"
            )

        elif age_hours <= 36:

            urgency_label = (
                "🟠 Posted within 36 hours"
            )

        elif age_hours <= 48:

            urgency_label = (
                "🟡 Posted within 48 hours"
            )

        elif age_hours <= 72:

            urgency_label = (
                "Normal freshness"
            )

        elif age_hours <= 168:

            urgency_label = (
                "Lower freshness"
            )

        else:

            urgency_label = (
                "⚪ Stale — posted more than 7 days ago"
            )

        # ------------------------------------------------------
        # OUTPUT FIELDS
        # ------------------------------------------------------

        item["future_timestamp"] = (
            future_timestamp
        )

        item["age_hours"] = round(
            age_hours,
            2,
        )

        item["age_minutes"] = round(
            age_minutes,
            0,
        )

        item["freshness_bucket"] = (
            bucket
        )

        item["freshness_priority"] = (
            priority
        )

        item["freshness_label"] = (
            urgency_label
        )

        item["is_fresh"] = (
            age_hours <= 48
        )

        return item

    # ==========================================================
    # ANALYZE MANY JOBS
    # ==========================================================

    @classmethod
    def analyze_jobs(
        cls,
        jobs,
        now=None,
    ):

        analyzed = [

            cls.analyze(
                job,
                now=now,
            )

            for job in (
                jobs or []
            )

        ]

        analyzed.sort(
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

        return analyzed

    # ==========================================================
    # FILTER BY AGE
    # ==========================================================

    @classmethod
    def filter_by_hours(
        cls,
        jobs,
        max_hours,
        now=None,
    ):

        analyzed = cls.analyze_jobs(
            jobs,
            now=now,
        )

        return [

            job

            for job in analyzed

            if (
                job.get(
                    "age_hours"
                ) is not None

                and

                job.get(
                    "age_hours"
                ) <= max_hours
            )

        ]

    # ==========================================================
    # SUMMARY
    # ==========================================================

    @classmethod
    def summary(
        cls,
        jobs,
        now=None,
    ):

        analyzed = cls.analyze_jobs(
            jobs,
            now=now,
        )

        summary = {

            "total":
                len(analyzed),

            "last_12_hours":
                0,

            "last_24_hours":
                0,

            "last_36_hours":
                0,

            "last_48_hours":
                0,

            "last_72_hours":
                0,

            "last_7_days":
                0,

            "stale":
                0,

            "unknown":
                0,

            "future_timestamp":
                0,

        }

        for job in analyzed:

            age = job.get(
                "age_hours"
            )

            if age is None:

                summary[
                    "unknown"
                ] += 1

                continue

            if job.get(
                "future_timestamp",
                False,
            ):

                summary[
                    "future_timestamp"
                ] += 1

            if age <= 12:

                summary[
                    "last_12_hours"
                ] += 1

                summary[
                    "last_24_hours"
                ] += 1

                summary[
                    "last_36_hours"
                ] += 1

                summary[
                    "last_48_hours"
                ] += 1

                summary[
                    "last_72_hours"
                ] += 1

                summary[
                    "last_7_days"
                ] += 1

            elif age <= 24:

                summary[
                    "last_24_hours"
                ] += 1

                summary[
                    "last_36_hours"
                ] += 1

                summary[
                    "last_48_hours"
                ] += 1

                summary[
                    "last_72_hours"
                ] += 1

                summary[
                    "last_7_days"
                ] += 1

            elif age <= 36:

                summary[
                    "last_36_hours"
                ] += 1

                summary[
                    "last_48_hours"
                ] += 1

                summary[
                    "last_72_hours"
                ] += 1

                summary[
                    "last_7_days"
                ] += 1

            elif age <= 48:

                summary[
                    "last_48_hours"
                ] += 1

                summary[
                    "last_72_hours"
                ] += 1

                summary[
                    "last_7_days"
                ] += 1

            elif age <= 72:

                summary[
                    "last_72_hours"
                ] += 1

                summary[
                    "last_7_days"
                ] += 1

            elif age <= 168:

                summary[
                    "last_7_days"
                ] += 1

            else:

                summary[
                    "stale"
                ] += 1

        return summary


# ==========================================================
# DIRECT TEST
# ==========================================================

if __name__ == "__main__":

    sample_jobs = [

        {
            "title":
                "Head of Sales",

            "posted_date":
                "2026-08-14T05:00:00Z",
        },

        {
            "title":
                "Sales Director",

            "posted_date":
                "2026-08-13T05:00:00Z",
        },

        {
            "title":
                "Head of Business Development",

            "posted_date":
                "2026-08-12T05:00:00Z",
        },

    ]

    results = (
        JobFreshnessEngine
        .analyze_jobs(
            sample_jobs
        )
    )

    print(
        "FRESHNESS TEST:"
    )

    for job in results:

        print(
            job["title"],
            "|",
            job[
                "freshness_bucket"
            ],
            "|",
            job[
                "freshness_label"
            ],
            "| Age:",
            job[
                "age_hours"
            ],
            "hrs",
        )

    print()
    print(
        "SUMMARY:"
    )

    print(
        JobFreshnessEngine.summary(
            sample_jobs
        )
    )
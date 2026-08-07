class ResumeTailoringEngine:

    def __init__(self):
        pass

    # --------------------------------------------------

    def extract_keywords(
        self,
        job
    ):

        text = " ".join(

            [

                str(job.get("role", "")),
                str(job.get("title", "")),
                str(job.get("description", "")),
                str(job.get("industry", ""))

            ]

        ).lower()

        keywords = []

        for word in text.split():

            word = word.strip(",.()[]{}:;!?/")

            if len(word) < 5:

                continue

            if word.isdigit():

                continue

            if word not in keywords:

                keywords.append(word)

        return keywords[:40]

    # --------------------------------------------------

    def tailor_resume(
        self,
        resume_text,
        job
    ):

        resume_lower = resume_text.lower()

        keywords = self.extract_keywords(job)

        missing = [

            keyword

            for keyword in keywords

            if keyword not in resume_lower

        ]

        matched = [

            keyword

            for keyword in keywords

            if keyword in resume_lower

        ]

        ats_score = round(

            (

                len(matched)
                /
                max(len(keywords), 1)

            ) * 100,

            1

        )

        return {

            "ats_score": ats_score,

            "matched_keywords": matched,

            "missing_keywords": missing,

            "recommended_keywords": keywords,

            "tailored_summary":

                "Executive leader with strong commercial, operational and strategic leadership experience aligned to "

                + job.get(
                    "role",
                    job.get(
                        "title",
                        "this opportunity"
                    )
                )

                + ". Prioritise these keywords: "

                + ", ".join(keywords[:12])

        }
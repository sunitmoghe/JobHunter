class ResumeTailoringEngine:

    def __init__(self):
        pass

    def extract_keywords(self, job):

        text = (
            job.get("description", "")
            + " "
            + job.get("role", "")
        )

        words = text.split()

        keywords = []

        for word in words:

            word = word.strip(",.()").lower()

            if len(word) > 4:

                if word not in keywords:

                    keywords.append(word)

        return keywords[:30]

    def tailor_resume(
        self,
        resume_text,
        job
    ):

        keywords = self.extract_keywords(job)

        suggestions = []

        for keyword in keywords:

            if keyword.lower() not in resume_text.lower():

                suggestions.append(keyword)

        return {

            "missing_keywords": suggestions,

            "recommended_keywords": keywords,

            "tailored_summary":

            (
                "Executive leader with extensive experience aligned "
                "to this opportunity. Resume should emphasize: "
                + ", ".join(keywords[:10])
            )

        }
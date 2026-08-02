class JobRecommendationEngine:

    def recommend(self, jobs, minimum_score=70):

        recommendations = []

        for job in jobs:

            score = job.get("executive_score", 0)

            if score >= minimum_score:

                recommendations.append(job)

        recommendations.sort(
            key=lambda x: x.get("executive_score", 0),
            reverse=True
        )

        return recommendations

    def top_recommendations(self, jobs, limit=20):

        return self.recommend(jobs)[:limit]
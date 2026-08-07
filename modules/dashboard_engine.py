import sqlite3
from pathlib import Path


class DashboardEngine:

    def __init__(self):

        self.db_path = Path("database/jobhunter.db")

    def _connect(self):

        return sqlite3.connect(self.db_path)

    def get_dashboard_stats(self):

        stats = {
            "total_jobs": 0,
            "saved_jobs": 0,
            "applied_jobs": 0,
            "countries": 0,
            "companies": 0,
            "avg_score": 0,
            "avg_opportunity": 0,
        }

        try:

            conn = self._connect()
            cur = conn.cursor()

            # ----------------------------
            # Jobs
            # ----------------------------

            try:

                cur.execute(
                    "SELECT COUNT(*) FROM jobs"
                )

                stats["total_jobs"] = cur.fetchone()[0]

            except:
                pass

            # ----------------------------
            # Saved Jobs
            # ----------------------------

            try:

                cur.execute(
                    "SELECT COUNT(*) FROM saved_jobs"
                )

                stats["saved_jobs"] = cur.fetchone()[0]

            except:
                pass

            # ----------------------------
            # Applications
            # ----------------------------

            try:

                cur.execute(
                    "SELECT COUNT(*) FROM applications"
                )

                stats["applied_jobs"] = cur.fetchone()[0]

            except:
                pass

            # ----------------------------
            # Countries
            # ----------------------------

            try:

                cur.execute(
                    "SELECT COUNT(DISTINCT country) FROM jobs"
                )

                stats["countries"] = cur.fetchone()[0]

            except:
                pass

            # ----------------------------
            # Companies
            # ----------------------------

            try:

                cur.execute(
                    "SELECT COUNT(DISTINCT company) FROM jobs"
                )

                stats["companies"] = cur.fetchone()[0]

            except:
                pass

            # ----------------------------
            # Average JobHunter Score
            # ----------------------------

            try:

                cur.execute(
                    """
                    SELECT AVG(jobhunter_score)
                    FROM jobs
                    """
                )

                value = cur.fetchone()[0]

                if value:
                    stats["avg_score"] = round(value, 1)

            except:
                pass

            # ----------------------------
            # Executive Opportunity
            # ----------------------------

            try:

                cur.execute(
                    """
                    SELECT AVG(opportunity_score)
                    FROM jobs
                    """
                )

                value = cur.fetchone()[0]

                if value:
                    stats["avg_opportunity"] = round(value, 1)

            except:
                pass

            conn.close()

        except:

            pass

        return stats
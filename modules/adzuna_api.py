import os
import requests
from dotenv import load_dotenv

load_dotenv()


class AdzunaAPI:

    def __init__(self):

        self.app_id = os.getenv("ADZUNA_APP_ID")
        self.app_key = os.getenv("ADZUNA_APP_KEY")

    def search_jobs(
        self,
        role,
        country="in",
        results=10
    ):

        if not self.app_id or not self.app_key:

            print("Adzuna credentials not configured.")

            return []

        url = (
            f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
            f"?app_id={self.app_id}"
            f"&app_key={self.app_key}"
            f"&results_per_page={results}"
            f"&what={role}"
            f"&content-type=application/json"
        )

        try:

            response = requests.get(
                url,
                timeout=5
            )

            response.raise_for_status()

            data = response.json()

        except requests.exceptions.Timeout:

            print(f"Timeout while searching {country}")

            return []

        except requests.exceptions.RequestException as e:

            print(f"Adzuna request failed for {country}: {e}")

            return []

        jobs = []

        for item in data.get("results", []):

            jobs.append(

                {
                    "role": item.get("title", ""),

                    "company": item.get(
                        "company",
                        {}
                    ).get(
                        "display_name",
                        "Unknown"
                    ),

                    "location": item.get(
                        "location",
                        {}
                    ).get(
                        "display_name",
                        ""
                    ),

                    "country": country.upper(),

                    "salary": (
                        f"{item.get('salary_min', '')} - {item.get('salary_max', '')}"
                        if item.get("salary_min")
                        else "Not Disclosed"
                    ),

                    "description": item.get(
                        "description",
                        ""
                    ),

                    "link": item.get(
                        "redirect_url",
                        ""
                    )
                }

            )

        return jobs


if __name__ == "__main__":

    api = AdzunaAPI()

    jobs = api.search_jobs(
        "Head of Sales"
    )

    print(f"Found {len(jobs)} jobs")

    for job in jobs:

        print(
            job["role"],
            "-",
            job["company"]
        )
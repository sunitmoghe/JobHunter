class ExecutiveSalaryEngine:

    def __init__(self):

        self.salary_data = {

            "Singapore": {
                "Head of Sales": (180000, 260000),
                "Sales Director": (160000, 240000),
                "VP Sales": (220000, 350000),
                "Chief Operating Officer": (280000, 500000)
            },

            "United Kingdom": {
                "Head of Sales": (90000, 150000),
                "Sales Director": (85000, 140000),
                "VP Sales": (140000, 220000),
                "Chief Operating Officer": (180000, 350000)
            },

            "Germany": {
                "Head of Sales": (100000, 170000),
                "Sales Director": (95000, 165000),
                "VP Sales": (150000, 240000),
                "Chief Operating Officer": (200000, 350000)
            },

            "United Arab Emirates": {
                "Head of Sales": (300000, 550000),
                "Sales Director": (280000, 500000),
                "VP Sales": (450000, 750000),
                "Chief Operating Officer": (600000, 1000000)
            }

        }

    def estimate_salary(

        self,

        role,

        country

    ):

        country_data = self.salary_data.get(country)

        if not country_data:

            return {

                "available": False,

                "minimum": None,

                "maximum": None

            }

        salary = country_data.get(role)

        if not salary:

            return {

                "available": False,

                "minimum": None,

                "maximum": None

            }

        return {

            "available": True,

            "minimum": salary[0],

            "maximum": salary[1]

        }

    def enrich_job(

        self,

        job

    ):

        country = job.get(

            "country",

            ""

        )

        role = job.get(

            "role",

            job.get(

                "title",

                ""

            )

        )

        salary = self.estimate_salary(

            role,

            country

        )

        job["salary_estimate"] = salary

        return job

    def enrich_jobs(

        self,

        jobs

    ):

        return [

            self.enrich_job(job)

            for job in jobs

        ]


if __name__ == "__main__":

    engine = ExecutiveSalaryEngine()

    sample = {

        "country": "Singapore",

        "role": "Head of Sales"

    }

    print(

        engine.enrich_job(sample)

    )
class SalaryIntelligence:


    def __init__(self):

        self.salary_database = {

            "Singapore": {

                "VP Sales": {
                    "low": 160000,
                    "average": 220000,
                    "high": 320000
                },

                "Head of Sales": {
                    "low": 140000,
                    "average": 200000,
                    "high": 280000
                },

                "Regional Sales Director": {
                    "low": 150000,
                    "average": 230000,
                    "high": 350000
                }

            },


            "UAE": {

                "VP Sales": {
                    "low": 500000,
                    "average": 750000,
                    "high": 1200000
                },

                "Head of Sales": {
                    "low": 400000,
                    "average": 650000,
                    "high": 1000000
                }

            },


            "Germany": {

                "VP Sales": {
                    "low": 120000,
                    "average": 170000,
                    "high": 250000
                },

                "Head of Sales": {
                    "low": 100000,
                    "average": 150000,
                    "high": 220000
                }

            },


            "India": {

                "VP Sales": {
                    "low": 3500000,
                    "average": 6000000,
                    "high": 12000000
                },

                "Head of Sales": {
                    "low": 2500000,
                    "average": 5000000,
                    "high": 9000000
                }

            }

        }



    def get_salary_benchmark(
        self,
        country,
        role
    ):

        country_data = self.salary_database.get(
            country,
            {}
        )


        role_data = country_data.get(
            role,
            {}
        )


        if role_data:

            return {

                "country": country,

                "role": role,

                "low": role_data["low"],

                "average": role_data["average"],

                "high": role_data["high"],

                "currency": self.get_currency(country)

            }


        return {

            "country": country,

            "role": role,

            "message": "Salary benchmark not available"

        }



    def get_currency(
        self,
        country
    ):


        currencies = {

            "Singapore": "SGD",

            "UAE": "AED",

            "Germany": "EUR",

            "India": "INR"

        }


        return currencies.get(
            country,
            "USD"
        )



    def compare_offer(
        self,
        country,
        role,
        offered_salary
    ):


        benchmark = self.get_salary_benchmark(
            country,
            role
        )


        if "average" not in benchmark:

            return benchmark



        average = benchmark["average"]


        if offered_salary >= average * 1.15:

            rating = "Excellent Offer"


        elif offered_salary >= average:

            rating = "Good Offer"


        else:

            rating = "Below Market"



        return {

            "offered_salary": offered_salary,

            "market_average": average,

            "rating": rating,

            "difference_percentage": round(
                (
                    (offered_salary - average)
                    /
                    average
                )
                * 100,
                2
            )

        }


def recommend_market_position(
    self,
    experience_years,
    leadership_level
):

    # Convert string experience like "23+ Years" to integer
    if isinstance(experience_years, str):
        import re

        match = re.search(r"\d+", experience_years)

        if match:
            experience_years = int(match.group())
        else:
            experience_years = 0

    if experience_years >= 20:

        return {

            "level": "Executive Leadership",

            "recommended_roles": [

                "VP Sales",

                "Regional Sales Director",

                "Chief Revenue Officer",

                "Head of Operations"

            ]

        }

    return {

        "level": "Senior Management",

        "recommended_roles": [

            "Sales Director",

            "Business Development Head"

        ]

    }
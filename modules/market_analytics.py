class MarketAnalytics:


    def __init__(self):

        self.market_data = {


            "Singapore": {

                "demand_score": 90,

                "salary_index": 90,

                "top_roles": [

                    "VP Sales",

                    "Regional Sales Director",

                    "Chief Revenue Officer"

                ],

                "skills": [

                    "SaaS Sales",

                    "Enterprise Selling",

                    "P&L Management",

                    "Digital Transformation"

                ]

            },


            "UAE": {

                "demand_score": 85,

                "salary_index": 85,

                "top_roles": [

                    "Head of Sales",

                    "Business Development Director",

                    "COO"

                ],

                "skills": [

                    "GCC Market Expansion",

                    "Enterprise Sales",

                    "Channel Management",

                    "Strategic Partnerships"

                ]

            },


            "Germany": {

                "demand_score": 82,

                "salary_index": 82,

                "top_roles": [

                    "Regional Sales Director",

                    "Sales Director",

                    "Country Manager"

                ],

                "skills": [

                    "Industry 4.0",

                    "Industrial Automation",

                    "B2B Sales",

                    "Digital Strategy"

                ]

            },


            "India": {

                "demand_score": 75,

                "salary_index": 70,

                "top_roles": [

                    "VP Sales",

                    "Business Head",

                    "COO"

                ],

                "skills": [

                    "Revenue Growth",

                    "Team Leadership",

                    "Operations Management"

                ]

            }


        }



    def get_country_analysis(
        self,
        country
    ):

        return self.market_data.get(

            country,

            {

                "message":
                "Market data not available"

            }

        )



    def get_top_markets(
        self
    ):

        markets = []


        for country, data in self.market_data.items():

            markets.append(

                {

                    "country": country,

                    "demand_score":
                    data["demand_score"],

                    "salary_index":
                    data["salary_index"]

                }

            )


        return sorted(

            markets,

            key=lambda x: x["demand_score"],

            reverse=True

        )



    def get_role_demand(
        self
    ):


        roles = {}


        for country, data in self.market_data.items():


            for role in data["top_roles"]:

                if role not in roles:

                    roles[role] = 0


                roles[role] += 1



        return sorted(

            roles.items(),

            key=lambda x: x[1],

            reverse=True

        )



    def get_skill_trends(
        self
    ):


        skills = {}


        for country, data in self.market_data.items():


            for skill in data["skills"]:

                if skill not in skills:

                    skills[skill] = 0


                skills[skill] += 1



        return sorted(

            skills.items(),

            key=lambda x: x[1],

            reverse=True

        )



    def executive_market_recommendation(
        self,
        experience_years,
        industries
    ):


        if experience_years >= 20:


            return {

                "recommended_markets": [

                    "Singapore",

                    "UAE",

                    "Germany"

                ],

                "recommended_strategy":

                "Target VP, Director and C-level roles with quantified revenue and P&L achievements."

            }



        return {

            "recommended_markets":

            [

                "India"

            ],

            "recommended_strategy":

            "Target senior management growth roles."

        }
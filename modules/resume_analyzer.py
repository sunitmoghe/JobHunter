import re


class ResumeAnalyzer:

    def __init__(self, resume_text):

        self.text = str(resume_text)

        self.lower_text = self.text.lower()

    # --------------------------------------------------

    def extract_name(self):

        for line in self.text.splitlines():

            line = line.strip()

            if len(line) > 3:

                return line

        return "Unknown"

    # --------------------------------------------------

    def extract_experience(self):

        patterns = [

            r"(\d+)\+?\s*years",

            r"(\d+)\s*yrs",

            r"experience\s*[:\-]?\s*(\d+)"

        ]

        for pattern in patterns:

            match = re.search(

                pattern,

                self.lower_text

            )

            if match:

                return f"{match.group(1)}+ Years"

        return "Not Found"

    # --------------------------------------------------

    def find_matches(
        self,
        items
    ):

        return sorted(

            {

                item

                for item in items

                if item.lower() in self.lower_text

            }

        )

    # --------------------------------------------------

    def analyze(self):

        skills = [

            "Business Development",
            "Strategic Sales",
            "Enterprise Sales",
            "Revenue Growth",
            "P&L",
            "CRM",
            "Customer Success",
            "Team Leadership",
            "Operations",
            "Shared Services",
            "SaaS",
            "Automation",
            "IoT",
            "Digital Transformation",
            "Key Account Management"

        ]

        industries = [

            "Telecom",
            "Technology",
            "Engineering",
            "Renewable Energy",
            "Manufacturing",
            "Industrial Automation",
            "Electronics",
            "Software"

        ]

        leadership = "Executive"

        return {

            "name": self.extract_name(),

            "experience": self.extract_experience(),

            "skills": self.find_matches(skills),

            "industries": self.find_matches(industries),

            "leadership": leadership,

            "word_count": len(self.text.split())

        }
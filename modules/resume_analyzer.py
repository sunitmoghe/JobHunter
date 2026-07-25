import re


class ResumeAnalyzer:

    def __init__(self, resume_text):
        self.text = resume_text
        self.lower_text = resume_text.lower()

    def extract_name(self):
        first_line = self.text.splitlines()[0].strip()
        return first_line

    def extract_experience(self):
        match = re.search(r'(\d+)\+?\s*years', self.lower_text)

        if match:
            return match.group(1) + "+ Years"

        return "Not Found"

    def find_matches(self, items):
        return sorted(
            {
                item
                for item in items
                if item.lower() in self.lower_text
            }
        )

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
            "Automation"
        ]

        industries = [
            "Telecom",
            "Technology",
            "Engineering",
            "Renewable Energy",
            "Manufacturing",
            "Industrial Automation"
        ]

        leadership = "Executive"

        return {
            "name": self.extract_name(),
            "experience": self.extract_experience(),
            "skills": self.find_matches(skills),
            "industries": self.find_matches(industries),
            "leadership": leadership
        }
import re
import json


class ResumeIntelligence:

    def __init__(self, resume_text):
        self.text = resume_text

    def extract_name(self):
        lines = [line.strip() for line in self.text.split("\n") if line.strip()]
        return lines[0] if lines else "Unknown"

    def extract_email(self):
        match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', self.text)
        return match.group(0) if match else ""

    def extract_phone(self):
        match = re.search(r'(\+?\d[\d\s\-]{8,}\d)', self.text)
        return match.group(0) if match else ""

    def extract_linkedin(self):
        match = re.search(r'linkedin\.com/[^\s]+', self.text, re.IGNORECASE)
        return match.group(0) if match else ""

    def extract_experience(self):
        match = re.search(r'(\d{1,2}\+?\s*years?)', self.text, re.IGNORECASE)
        if match:
            return match.group(0)
        return "Unknown"

    def extract_skills(self):
        found = []

        try:
            with open("resources/skills.json", "r", encoding="utf-8") as f:
                skills = json.load(f)

            text = self.text.lower()

            for category in skills:
                for skill in skills[category]:
                    if skill.lower() in text:
                        found.append(skill)

        except Exception as e:
            print("Skills file error:", e)

        return sorted(set(found))

    def build_profile(self):
        return {
            "name": self.extract_name(),
            "email": self.extract_email(),
            "phone": self.extract_phone(),
            "linkedin": self.extract_linkedin(),
            "experience": self.extract_experience(),
            "skills": self.extract_skills()
        }


if __name__ == "__main__":

    from modules.resume_parser import ResumeParser

    parser = ResumeParser("temp_resume.pdf")

    resume_text = parser.read_resume()

    engine = ResumeIntelligence(resume_text)

    profile = engine.build_profile()

    print("\n===== EXECUTIVE PROFILE =====\n")

    for key, value in profile.items():
        print(f"{key}: {value}")
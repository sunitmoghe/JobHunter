import json
import os
import re


class ResumeIntelligence:

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

    def extract_email(self):

        match = re.search(
            r"[\w\.-]+@[\w\.-]+\.\w+",
            self.text
        )

        return match.group(0) if match else ""

    # --------------------------------------------------

    def extract_phone(self):

        match = re.search(
            r"(\+?\d[\d\s\-\(\)]{8,}\d)",
            self.text
        )

        return match.group(0).strip() if match else ""

    # --------------------------------------------------

    def extract_linkedin(self):

        match = re.search(
            r"(https?://)?(www\.)?linkedin\.com/[^\s]+",
            self.text,
            re.IGNORECASE
        )

        return match.group(0).rstrip(".,)") if match else ""

    # --------------------------------------------------

    def extract_experience(self):

        match = re.search(
            r"(\d+)\+?\s*years",
            self.lower_text
        )

        if match:
            return f"{match.group(1)}+ Years"

        return "Unknown"

    # --------------------------------------------------

    def extract_skills(self):

        found = []

        skills_file = os.path.join(
            "resources",
            "skills.json"
        )

        if not os.path.exists(skills_file):
            return found

        try:

            with open(
                skills_file,
                "r",
                encoding="utf-8"
            ) as file:

                skills_data = json.load(file)

            if isinstance(skills_data, dict):

                for values in skills_data.values():

                    if not isinstance(values, list):
                        continue

                    for skill in values:

                        skill = str(skill).strip()

                        if skill and skill.lower() in self.lower_text:
                            found.append(skill)

            elif isinstance(skills_data, list):

                for skill in skills_data:

                    skill = str(skill).strip()

                    if skill and skill.lower() in self.lower_text:
                        found.append(skill)

        except Exception:

            return sorted(set(found))

        return sorted(set(found))

    # --------------------------------------------------

    def build_profile(self):

        return {

            "name": self.extract_name(),

            "email": self.extract_email(),

            "phone": self.extract_phone(),

            "linkedin": self.extract_linkedin(),

            "experience": self.extract_experience(),

            "skills": self.extract_skills(),

            "word_count": len(
                self.text.split()
            )

        }


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    from modules.resume_parser import ResumeParser

    resume_file = None

    data_folder = "data"

    if os.path.exists(data_folder):

        for file_name in os.listdir(data_folder):

            if file_name.lower().endswith(
                (".pdf", ".docx")
            ):

                resume_file = os.path.join(
                    data_folder,
                    file_name
                )

                break

    if resume_file is None:

        raise FileNotFoundError(
            "No PDF or DOCX resume found inside data folder."
        )

    parser = ResumeParser(
        resume_file
    )

    resume = parser.read_resume()

    profile = ResumeIntelligence(
        resume
    ).build_profile()

    print(
        json.dumps(
            profile,
            indent=4,
            ensure_ascii=False
        )
    )
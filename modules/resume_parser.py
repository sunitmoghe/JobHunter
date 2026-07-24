from pypdf import PdfReader
import os


class ResumeParser:

    def __init__(self, resume_path):
        self.resume_path = resume_path

    def read_resume(self):

        if not os.path.exists(self.resume_path):
            raise FileNotFoundError(
                f"Resume not found: {self.resume_path}"
            )

        reader = PdfReader(self.resume_path)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text

    def extract_profile(self):

        text = self.read_resume()

        profile = {
            "characters": len(text),
            "words": len(text.split()),
            "preview": text[:500]
        }

        return profile


if __name__ == "__main__":

    parser = ResumeParser("data/Sunit CV.pdf")

    profile = parser.extract_profile()

    print("\nResume Statistics")
    print("-----------------")
    print(f"Characters : {profile['characters']}")
    print(f"Words      : {profile['words']}")
    print("\nPreview:\n")
    print(profile["preview"])

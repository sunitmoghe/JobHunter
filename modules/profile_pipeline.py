from modules.resume_parser import ResumeParser
from modules.resume_intelligence import ResumeIntelligence
from modules.database import DatabaseManager


def process_resume(resume_file):

    # Automatically detects PDF or DOCX
    parser = ResumeParser(resume_file)

    resume_text = parser.read_resume()

    intelligence = ResumeIntelligence(resume_text)

    profile = intelligence.build_profile()

    db = DatabaseManager()

    db.save_profile(profile)

    db.close()

    return profile


if __name__ == "__main__":

    import os

    data_folder = "data"

    supported = [".pdf", ".docx", ".doc"]

    resume_file = None

    if os.path.exists(data_folder):

        for file in os.listdir(data_folder):

            extension = os.path.splitext(file)[1].lower()

            if extension in supported:

                resume_file = os.path.join(data_folder, file)

                break

    if resume_file is None:

        print("\nNo PDF/DOCX resume found inside data folder.\n")

    else:

        profile = process_resume(resume_file)

        print("\nPROFILE SAVED SUCCESSFULLY\n")

        for key, value in profile.items():

            print(key, ":", value)
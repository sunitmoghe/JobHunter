from modules.resume_parser import ResumeParser
from modules.resume_intelligence import ResumeIntelligence
from modules.database import DatabaseManager


def process_resume(resume_file):

    # Read PDF
    parser = ResumeParser(resume_file)

    resume_text = parser.read_resume()


    # Extract profile
    intelligence = ResumeIntelligence(resume_text)

    profile = intelligence.build_profile()


    # Save to database
    db = DatabaseManager()

    db.save_profile(profile)

    db.close()


    return profile



if __name__ == "__main__":

    profile = process_resume("temp_resume.pdf")

    print("\nPROFILE SAVED SUCCESSFULLY\n")

    for key, value in profile.items():
        print(key, ":", value)
import os

from pypdf import PdfReader
from docx import Document


class ResumeParser:

    def __init__(self, resume_path):

        self.resume_path = resume_path

    # --------------------------------------------------

    def _read_pdf(self):

        reader = PdfReader(self.resume_path)

        pages = []

        for page in reader.pages:

            try:

                text = page.extract_text()

                if text:
                    pages.append(text)

            except Exception:
                pass

        return "\n".join(pages), len(reader.pages)

    # --------------------------------------------------

    def _read_docx(self):

        document = Document(self.resume_path)

        paragraphs = []

        for paragraph in document.paragraphs:

            if paragraph.text.strip():

                paragraphs.append(paragraph.text)

        return "\n".join(paragraphs), 1

    # --------------------------------------------------

    def read_resume(self):

        if not os.path.exists(self.resume_path):

            raise FileNotFoundError(
                f"Resume not found: {self.resume_path}"
            )

        extension = os.path.splitext(
            self.resume_path
        )[1].lower()

        if extension == ".pdf":

            text, _ = self._read_pdf()

            return text

        elif extension == ".docx":

            text, _ = self._read_docx()

            return text

        else:

            raise ValueError(

                "Only PDF and DOCX resumes are supported."

            )

    # --------------------------------------------------

    def extract_profile(self):

        extension = os.path.splitext(
            self.resume_path
        )[1].lower()

        if extension == ".pdf":

            text, pages = self._read_pdf()

        elif extension == ".docx":

            text, pages = self._read_docx()

        else:

            raise ValueError(

                "Only PDF and DOCX resumes are supported."

            )

        return {

            "text": text,

            "characters": len(text),

            "words": len(text.split()),

            "pages": pages,

            "file_type": extension.replace(".", "").upper(),

            "preview": text[:1000]

        }


if __name__ == "__main__":

    data_folder = "data"

    supported = (

        ".pdf",

        ".docx"

    )

    resume_file = None

    if os.path.exists(data_folder):

        for file in os.listdir(data_folder):

            if file.lower().endswith(supported):

                resume_file = os.path.join(

                    data_folder,

                    file

                )

                break

    if resume_file is None:

        raise FileNotFoundError(

            "No PDF or DOCX resume found inside the data folder."

        )

    parser = ResumeParser(resume_file)

    profile = parser.extract_profile()

    print(profile)
from collections import Counter
import re


class ATSMatcher:
    def __init__(self, resume_text, job_description):
        self.resume_text = resume_text.lower()
        self.job_description = job_description.lower()

    def tokenize(self, text):
        return re.findall(r"\b[a-zA-Z0-9+#.-]+\b", text)

    def calculate_match(self):
        resume_words = Counter(self.tokenize(self.resume_text))
        jd_words = Counter(self.tokenize(self.job_description))

        matched = []
        missing = []

        for word in sorted(jd_words.keys()):
            if len(word) < 3:
                continue

            if word in resume_words:
                matched.append(word)
            else:
                missing.append(word)

        total = len(matched) + len(missing)
        score = round((len(matched) / total) * 100, 2) if total else 0

        return {
            "score": score,
            "matched": matched,
            "missing": missing,
        }
import json
from pathlib import Path


class SkillIntelligence:

    def __init__(self):

        path = Path(
            "resources/skill_mapping.json"
        )

        try:

            with open(

                path,

                "r",

                encoding="utf-8"

            ) as f:

                self.mapping = json.load(f)

        except Exception:

            self.mapping = {}

    # --------------------------------------------------

    def normalize_skills(
        self,
        skills
    ):

        expanded = set()

        if isinstance(skills, str):

            skills = [

                skill.strip()

                for skill in skills.split(",")

                if skill.strip()

            ]

        for skill in skills:

            skill = str(skill).lower().strip()

            if not skill:

                continue

            expanded.add(skill)

            for category, keywords in self.mapping.items():

                keyword_list = [

                    str(keyword).lower()

                    for keyword in keywords

                ]

                if skill in keyword_list:

                    expanded.add(

                        str(category).lower()

                    )

        return expanded
import json
from pathlib import Path


class SkillIntelligence:


    def __init__(self):

        path = Path(
            "resources/skill_mapping.json"
        )

        with open(path, "r") as f:
            self.mapping = json.load(f)



    def normalize_skills(self, skills):

        expanded = set()


        for skill in skills:

            skill = skill.lower().strip()

            expanded.add(skill)


            for category, keywords in self.mapping.items():

                if skill in [
                    x.lower()
                    for x in keywords
                ]:
                    expanded.add(
                        category.lower()
                    )


        return expanded
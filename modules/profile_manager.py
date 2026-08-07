import json
import os
from datetime import datetime


class ProfileManager:

    def __init__(self):

        self.data_folder = "data"

        self.profile_file = os.path.join(
            self.data_folder,
            "executive_profile.json"
        )

        os.makedirs(
            self.data_folder,
            exist_ok=True
        )

    # --------------------------------------------------

    def save_profile(
        self,
        profile
    ):

        try:

            profile["last_updated"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            )

            with open(
                self.profile_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    profile,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            return True

        except Exception as e:

            print(e)

            return False

    # --------------------------------------------------

    def load_profile(self):

        if not os.path.exists(
            self.profile_file
        ):

            return {}

        try:

            with open(
                self.profile_file,
                "r",
                encoding="utf-8"
            ) as file:

                profile = json.load(file)

                if isinstance(profile, dict):

                    return profile

        except Exception as e:

            print(e)

        return {}

    # --------------------------------------------------

    def update_profile(
        self,
        updates
    ):

        profile = self.load_profile()

        profile.update(updates)

        return self.save_profile(profile)

    # --------------------------------------------------

    def profile_exists(self):

        return os.path.isfile(
            self.profile_file
        )

    # --------------------------------------------------

    def delete_profile(self):

        try:

            if os.path.exists(
                self.profile_file
            ):

                os.remove(
                    self.profile_file
                )

            return True

        except Exception as e:

            print(e)

            return False

    # --------------------------------------------------

    def clear_profile(self):

        return self.save_profile({})

    # --------------------------------------------------

    def get_value(
        self,
        key,
        default=None
    ):

        profile = self.load_profile()

        return profile.get(
            key,
            default
        )

    # --------------------------------------------------

    def set_value(
        self,
        key,
        value
    ):

        profile = self.load_profile()

        profile[key] = value

        return self.save_profile(profile)

    # --------------------------------------------------

    def profile_summary(self):

        profile = self.load_profile()

        return {

            "name": profile.get("name", ""),

            "current_role": profile.get("current_role", ""),

            "experience": profile.get("experience", ""),

            "skills": len(
                profile.get(
                    "skills",
                    []
                )
            ),

            "last_updated": profile.get(
                "last_updated",
                ""
            )

        }


# --------------------------------------------------

if __name__ == "__main__":

    manager = ProfileManager()

    sample = {

        "name": "Sunit Moghe",

        "current_role": "Head of Sales",

        "experience": "23+ Years",

        "skills": [

            "Sales",

            "Leadership",

            "Operations"

        ]

    }

    manager.save_profile(sample)

    print(manager.profile_summary())
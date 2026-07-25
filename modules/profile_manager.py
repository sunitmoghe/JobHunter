import json
import os


class ProfileManager:

    def __init__(self):

        self.profile_file = os.path.join(
            "data",
            "executive_profile.json"
        )

    def save_profile(
        self,
        profile
    ):

        os.makedirs(
            "data",
            exist_ok=True
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

    def load_profile(self):

        if not os.path.exists(
            self.profile_file
        ):

            return {}

        with open(
            self.profile_file,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def profile_exists(self):

        return os.path.exists(
            self.profile_file
        )

    def delete_profile(self):

        if os.path.exists(
            self.profile_file
        ):

            os.remove(
                self.profile_file
            )
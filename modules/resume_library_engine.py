import json
import os
import uuid
from datetime import datetime


class ResumeLibraryEngine:

    def __init__(
        self,
        directory="data/resume_library",
        metadata_file="data/resume_library.json",
    ):

        self.directory = directory
        self.metadata_file = metadata_file

        os.makedirs(
            self.directory,
            exist_ok=True,
        )

        metadata_dir = os.path.dirname(
            self.metadata_file
        )

        if metadata_dir:

            os.makedirs(
                metadata_dir,
                exist_ok=True,
            )

        if not os.path.exists(
            self.metadata_file
        ):

            self._save_metadata([])

    # ==========================================================
    # INTERNAL STORAGE
    # ==========================================================

    def _load_metadata(self):

        try:

            with open(
                self.metadata_file,
                "r",
                encoding="utf-8",
            ) as file:

                data = json.load(file)

                if isinstance(
                    data,
                    list,
                ):

                    return data

        except Exception:

            pass

        return []

    def _save_metadata(
        self,
        resumes,
    ):

        with open(
            self.metadata_file,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                resumes,
                file,
                indent=4,
                ensure_ascii=False,
            )

    # ==========================================================
    # ADD RESUME
    # ==========================================================

    def add_resume(
        self,
        file_bytes,
        original_filename,
        resume_name=None,
        target_roles=None,
        target_countries=None,
        industries=None,
    ):

        if not file_bytes:

            raise ValueError(
                "Resume file is empty."
            )

        original_filename = str(
            original_filename or ""
        ).strip()

        if not original_filename:

            raise ValueError(
                "Original filename is required."
            )

        extension = os.path.splitext(
            original_filename
        )[1].lower()

        allowed_extensions = {
            ".pdf",
            ".docx",
            ".doc",
        }

        if extension not in allowed_extensions:

            raise ValueError(
                "Supported resume formats are PDF, DOCX and DOC."
            )

        resume_id = str(
            uuid.uuid4()
        )

        safe_name = (
            resume_name
            or
            os.path.splitext(
                original_filename
            )[0]
        )

        safe_name = (
            str(safe_name)
            .strip()
        )

        filename = (
            f"{resume_id}{extension}"
        )

        file_path = os.path.join(
            self.directory,
            filename,
        )

        with open(
            file_path,
            "wb",
        ) as file:

            file.write(
                file_bytes
            )

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )

        record = {

            "resume_id":
                resume_id,

            "resume_name":
                safe_name,

            "original_filename":
                original_filename,

            "file_path":
                file_path,

            "format":
                extension.lstrip(".").upper(),

            "target_roles":
                self._normalize_list(
                    target_roles
                ),

            "target_countries":
                self._normalize_list(
                    target_countries
                ),

            "industries":
                self._normalize_list(
                    industries
                ),

            "ats_baseline_score":
                None,

            "status":
                "Active",

            "created_at":
                now,

            "updated_at":
                now,

        }

        resumes = self._load_metadata()

        resumes.append(
            record
        )

        self._save_metadata(
            resumes
        )

        return record

    # ==========================================================
    # LIST
    # ==========================================================

    def get_all_resumes(
        self,
        include_archived=True,
    ):

        resumes = self._load_metadata()

        if include_archived:

            return resumes

        return [
            resume
            for resume in resumes
            if resume.get(
                "status",
                "Active",
            ) == "Active"
        ]

    # ==========================================================
    # GET ONE
    # ==========================================================

    def get_resume(
        self,
        resume_id,
    ):

        for resume in self._load_metadata():

            if resume.get(
                "resume_id"
            ) == resume_id:

                return resume

        return None

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update_resume(
        self,
        resume_id,
        updates,
    ):

        resumes = self._load_metadata()

        for resume in resumes:

            if resume.get(
                "resume_id"
            ) == resume_id:

                allowed_fields = {
                    "resume_name",
                    "target_roles",
                    "target_countries",
                    "industries",
                    "ats_baseline_score",
                }

                for key, value in (
                    updates or {}
                ).items():

                    if key in allowed_fields:

                        if key in {
                            "target_roles",
                            "target_countries",
                            "industries",
                        }:

                            value = (
                                self._normalize_list(
                                    value
                                )
                            )

                        resume[key] = value

                resume["updated_at"] = (
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M"
                    )
                )

                self._save_metadata(
                    resumes
                )

                return True

        return False

    # ==========================================================
    # ARCHIVE
    # ==========================================================

    def archive_resume(
        self,
        resume_id,
    ):

        return self._set_status(
            resume_id,
            "Archived",
        )

    def activate_resume(
        self,
        resume_id,
    ):

        return self._set_status(
            resume_id,
            "Active",
        )

    def _set_status(
        self,
        resume_id,
        status,
    ):

        resumes = self._load_metadata()

        for resume in resumes:

            if resume.get(
                "resume_id"
            ) == resume_id:

                resume["status"] = status

                resume["updated_at"] = (
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M"
                    )
                )

                self._save_metadata(
                    resumes
                )

                return True

        return False

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete_resume(
        self,
        resume_id,
    ):

        resumes = self._load_metadata()

        target = None

        for resume in resumes:

            if resume.get(
                "resume_id"
            ) == resume_id:

                target = resume
                break

        if target is None:

            return False

        file_path = target.get(
            "file_path",
            "",
        )

        if file_path and os.path.exists(
            file_path
        ):

            try:

                os.remove(
                    file_path
                )

            except OSError:

                pass

        resumes = [
            resume
            for resume in resumes
            if resume.get(
                "resume_id"
            ) != resume_id
        ]

        self._save_metadata(
            resumes
        )

        return True

    # ==========================================================
    # FILE ACCESS
    # ==========================================================

    def get_file_path(
        self,
        resume_id,
    ):

        resume = self.get_resume(
            resume_id
        )

        if not resume:

            return None

        path = resume.get(
            "file_path"
        )

        if path and os.path.exists(
            path
        ):

            return path

        return None

    # ==========================================================
    # HELPERS
    # ==========================================================

    @staticmethod
    def _normalize_list(
        value,
    ):

        if value is None:

            return []

        if isinstance(
            value,
            str,
        ):

            return [
                item.strip()
                for item in value.split(",")
                if item.strip()
            ]

        if isinstance(
            value,
            (list, tuple, set),
        ):

            return [
                str(item).strip()
                for item in value
                if str(item).strip()
            ]

        return [
            str(value).strip()
        ]


# ==========================================================
# DIRECT TEST
# ==========================================================

if __name__ == "__main__":

    engine = ResumeLibraryEngine()

    print(
        "Resume Library Engine: OK"
    )

    print(
        "Resume records:",
        len(
            engine.get_all_resumes()
        )
    )
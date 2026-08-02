import pandas as pd
import json
import os
from datetime import datetime


class JobExporter:

    def __init__(self):

        self.export_folder = "exports"

        os.makedirs(
            self.export_folder,
            exist_ok=True
        )

    def _timestamp(self):

        return datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

    def export_csv(
        self,
        jobs,
        filename=None
    ):

        if not jobs:
            return None

        if filename is None:

            filename = (
                f"ExecutiveJobs_{self._timestamp()}.csv"
            )

        path = os.path.join(
            self.export_folder,
            filename
        )

        df = pd.DataFrame(jobs)

        df.to_csv(
            path,
            index=False,
            encoding="utf-8-sig"
        )

        return path

    def export_excel(
        self,
        jobs,
        filename=None
    ):

        if not jobs:
            return None

        if filename is None:

            filename = (
                f"ExecutiveJobs_{self._timestamp()}.xlsx"
            )

        path = os.path.join(
            self.export_folder,
            filename
        )

        df = pd.DataFrame(jobs)

        with pd.ExcelWriter(
            path,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                index=False,
                sheet_name="Executive Jobs"
            )

        return path

    def export_json(
        self,
        jobs,
        filename=None
    ):

        if not jobs:
            return None

        if filename is None:

            filename = (
                f"ExecutiveJobs_{self._timestamp()}.json"
            )

        path = os.path.join(
            self.export_folder,
            filename
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                jobs,
                f,
                indent=4,
                ensure_ascii=False
            )

        return path

    def export_all(
        self,
        jobs
    ):

        return {

            "csv": self.export_csv(jobs),

            "excel": self.export_excel(jobs),

            "json": self.export_json(jobs)

        }


if __name__ == "__main__":

    sample_jobs = [

        {
            "role": "Head of Sales",
            "company": "Microsoft",
            "country": "Singapore",
            "executive_score": 96
        },

        {
            "role": "Regional Director",
            "company": "Siemens",
            "country": "Germany",
            "executive_score": 92
        }

    ]

    exporter = JobExporter()

    files = exporter.export_all(
        sample_jobs
    )

    print(files)
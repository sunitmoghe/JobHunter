import re


class JobNormalizer:

    @staticmethod
    def normalize(job):

        if not isinstance(job, dict):
            return {}

        normalized = dict(job)

        # --------------------------------------------------
        # TITLE
        # --------------------------------------------------

        title = (
            normalized.get("title")
            or normalized.get("role")
            or normalized.get("job_title")
            or "Executive Position"
        )

        normalized["title"] = str(
            title
        ).strip()


        # --------------------------------------------------
        # COMPANY
        # --------------------------------------------------

        normalized["company"] = str(
            normalized.get(
                "company",
                "Company not specified",
            )
        ).strip()


        # --------------------------------------------------
        # LOCATION
        # --------------------------------------------------

        normalized["location"] = str(
            normalized.get(
                "location",
                "",
            )
        ).strip()


        # --------------------------------------------------
        # APPLY URL
        # --------------------------------------------------

        possible_urls = [
            normalized.get("apply_link"),
            normalized.get("url"),
            normalized.get("redirect_url"),
            normalized.get("job_url"),
            normalized.get("link"),
        ]

        apply_url = ""

        for value in possible_urls:

            if not value:
                continue

            value = str(value).strip()

            # Remove Markdown link wrapper:
            # [text](https://...)
            match = re.search(
                r"\((https?://[^)]+)\)",
                value,
            )

            if match:

                value = match.group(1)

            # Remove accidental surrounding brackets
            value = value.strip(
                "[]()\"'"
            )

            if value.startswith(
                "http://"
            ) or value.startswith(
                "https://"
            ):

                apply_url = value

                break


        normalized["apply_link"] = (
            apply_url
        )


        # --------------------------------------------------
        # APPLY LINK STATUS
        # --------------------------------------------------

        normalized["has_apply_link"] = bool(
            apply_url
        )


        # --------------------------------------------------
        # DESCRIPTION
        # --------------------------------------------------

        normalized["description"] = str(
            normalized.get(
                "description",
                "",
            )
        ).strip()


        # --------------------------------------------------
        # SOURCE
        # --------------------------------------------------

        normalized["source"] = str(
            normalized.get(
                "source",
                "",
            )
        ).strip()


        return normalized


    @staticmethod
    def normalize_many(jobs):

        if not isinstance(
            jobs,
            list,
        ):

            return []

        return [
            JobNormalizer.normalize(job)
            for job in jobs
            if isinstance(
                job,
                dict,
            )
        ]
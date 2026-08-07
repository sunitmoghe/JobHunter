import json
import os
import time
import threading


class JobCache:

    def __init__(self):

        self.cache_dir = "database"

        self.cache_file = os.path.join(
            self.cache_dir,
            "job_cache.json"
        )

        self.expiry_seconds = 1800

        self.lock = threading.Lock()

        self._ensure_cache()

    # --------------------------------------------------

    def _ensure_cache(self):

        os.makedirs(
            self.cache_dir,
            exist_ok=True
        )

        if not os.path.exists(self.cache_file):

            with open(
                self.cache_file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    {},
                    f,
                    indent=4
                )

    # --------------------------------------------------

    def _load(self):

        self._ensure_cache()

        try:

            with open(
                self.cache_file,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

                if isinstance(data, dict):

                    return data

        except Exception as e:

            print(e)

        return {}

    # --------------------------------------------------

    def _save(
        self,
        cache
    ):

        try:

            with self.lock:

                with open(
                    self.cache_file,
                    "w",
                    encoding="utf-8"
                ) as f:

                    json.dump(
                        cache,
                        f,
                        indent=4,
                        ensure_ascii=False
                    )

            return True

        except Exception as e:

            print(e)

            return False

    # --------------------------------------------------

    def _make_key(
        self,
        role,
        countries=None
    ):

        role = str(role).lower().strip()

        if countries:

            country_key = ",".join(
                sorted(
                    [
                        str(c).lower()
                        for c in countries
                    ]
                )
            )

            return f"{role}|{country_key}"

        return role

    # --------------------------------------------------

    def save_jobs(
        self,
        role,
        jobs,
        countries=None
    ):

        cache = self._load()

        key = self._make_key(
            role,
            countries
        )

        cache[key] = {

            "timestamp": time.time(),

            "count": len(jobs),

            "jobs": jobs

        }

        self._save(cache)

    # --------------------------------------------------

    def get_jobs(
        self,
        role,
        countries=None
    ):

        cache = self._load()

        key = self._make_key(
            role,
            countries
        )

        if key not in cache:

            return None

        record = cache[key]

        age = time.time() - record.get(
            "timestamp",
            0
        )

        if age > self.expiry_seconds:

            del cache[key]

            self._save(cache)

            return None

        return record.get(
            "jobs",
            []
        )

    # --------------------------------------------------

    def delete(
        self,
        role,
        countries=None
    ):

        cache = self._load()

        key = self._make_key(
            role,
            countries
        )

        if key in cache:

            del cache[key]

            self._save(cache)

    # --------------------------------------------------

    def cleanup(self):

        cache = self._load()

        now = time.time()

        remove = []

        for key, value in cache.items():

            age = now - value.get(
                "timestamp",
                0
            )

            if age > self.expiry_seconds:

                remove.append(key)

        for key in remove:

            del cache[key]

        self._save(cache)

        return len(remove)

    # --------------------------------------------------

    def clear_cache(self):

        self._save({})

    # --------------------------------------------------

    def statistics(self):

        cache = self._load()

        total_jobs = sum(

            item.get(
                "count",
                0
            )

            for item in cache.values()

        )

        return {

            "cached_roles": len(cache),

            "cached_jobs": total_jobs,

            "expiry_minutes": self.expiry_seconds // 60

        }


# --------------------------------------------------

if __name__ == "__main__":

    cache = JobCache()

    sample = [

        {

            "company": "Microsoft",

            "role": "Head of Sales"

        }

    ]

    cache.save_jobs(

        "Head of Sales",

        sample,

        [

            "Singapore",

            "Germany"

        ]

    )

    print(cache.statistics())

    print(

        cache.get_jobs(

            "Head of Sales",

            [

                "Germany",

                "Singapore"

            ]

        )

    )
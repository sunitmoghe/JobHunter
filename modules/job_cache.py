import json
import os
import time


class JobCache:

    def __init__(self):

        self.cache_dir = "database"

        self.cache_file = os.path.join(
            self.cache_dir,
            "job_cache.json"
        )

        self.expiry_seconds = 1800

        self._ensure_cache()

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

    def _load(self):

        self._ensure_cache()

        try:

            with open(
                self.cache_file,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except Exception:

            return {}

    def _save(
        self,
        cache
    ):

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

    def save_jobs(
        self,
        role,
        jobs
    ):

        cache = self._load()

        cache[role] = {

            "timestamp": time.time(),

            "jobs": jobs

        }

        self._save(cache)

    def get_jobs(
        self,
        role
    ):

        cache = self._load()

        if role not in cache:

            return None

        record = cache[role]

        age = time.time() - record["timestamp"]

        if age > self.expiry_seconds:

            del cache[role]

            self._save(cache)

            return None

        return record["jobs"]

    def clear_cache(self):

        self._save({})

    def statistics(self):

        cache = self._load()

        return {

            "cached_roles": len(cache),

            "expiry_minutes": self.expiry_seconds // 60

        }


if __name__ == "__main__":

    cache = JobCache()

    print(cache.statistics())
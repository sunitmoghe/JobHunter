import time


class JobCache:

    def __init__(self):

        self.cache = {}

        self.expiry = 1800

    def save(
        self,
        key,
        jobs
    ):

        self.cache[key] = {

            "timestamp": time.time(),

            "jobs": jobs

        }

    def get(
        self,
        key
    ):

        if key not in self.cache:

            return None

        record = self.cache[key]

        age = time.time() - record["timestamp"]

        if age > self.expiry:

            del self.cache[key]

            return None

        return record["jobs"]

    def clear(self):

        self.cache = {}

    def exists(
        self,
        key
    ):

        return self.get(key) is not None

    def size(self):

        return len(self.cache)

    def statistics(self):

        return {

            "cached_searches": len(self.cache),

            "expiry_seconds": self.expiry

        }
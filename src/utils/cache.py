from typing import Any
from cachetools import TTLCache

class Cache:
    def __init__(self, maxsize: float, timeout: float) -> None:
        self.cache = TTLCache(maxsize, ttl=timeout)
    
    def get_data(self, key: str):
        if key not in self.cache:
            return None
        return self.cache[key]

    def set_data(self, key: str, value: Any):
        self.cache[key] = value

cache = Cache(maxsize=1024, timeout=300)
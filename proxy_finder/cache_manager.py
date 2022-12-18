import shelve
from pathlib import Path
from typing import List

from proxy_finder.abstract import ProxyInfo

class CacheManager:

    def __init__(self) -> None:
        temp_path = Path('./proxy_finder/temp')
        temp_path.mkdir(exist_ok=True)
        self._cache_path = Path.joinpath(Path.cwd(), temp_path)

    def write_cache(self, data: ProxyInfo) -> bool:
        """Write the cache, returns true if successful"""

        with self._cache_path.open('w') as cache_file:
            pass


    def get_cache(self, key) -> ProxyInfo:
        """Returns cache using a key"""
        pass

    def get_cache_names(self, key) -> List:
        """Returns cache names in a list"""
        pass

    def delete_cache(self, key: str) -> bool:
        """Deletes 1 cache item using a key"""
        pass

    def delete_all_cache(self) -> bool:
        """Deletes all cached items"""
        pass
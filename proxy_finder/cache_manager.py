import shelve
from pathlib import Path
from typing import List
from datetime import date

from proxy_finder.abstract import ProxyInfo
from proxy_finder.utils.formatter import format_sitename, format_date

class CacheManager:

    def __init__(self) -> None:
        temp_path = Path('./proxy_finder/temp')
        temp_path.mkdir(exist_ok=True)
        self._cache_path = Path.joinpath(Path.cwd(), temp_path)

    def write_cache(self, data: ProxyInfo) -> bool:
        """Write the cache, returns true if successful"""
        # site = format_sitename(data.meta.source_url)
        today = format_date(date().today())
        file_name = format_sitename(data.meta.source_url)
        path_to_file = Path.joinpath(self._cache_path, file_name)
        try:
            with shelve.open(path_to_file._str) as cache_file:
                cache_file[today] = data
        except:
            # logger here
            return False

        return True


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
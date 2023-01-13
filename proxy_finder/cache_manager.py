import shelve
from pathlib import Path
from typing import List, Optional
from datetime import date

from proxy_finder.abstract import ProxyInfo
from proxy_finder.utils.formatter import format_sitename, format_date, country_code

class CacheManager:

    def __init__(self) -> None:
        temp_path = Path('./proxy_finder/temp')
        self._cache_path = Path.joinpath(Path.cwd(), temp_path)
        self._cache_path.mkdir(exist_ok=True)

    def write_cache(self, data: ProxyInfo, name: str=None) -> bool:
        """Write the cache, returns true if successful"""
        # site = format_sitename(data.meta.source_url)
        file_name = format_date(date.today())
        if name:
            file_name = f'{name}_{file_name}' 
        key = format_sitename(data.meta.source_url)
        path_to_file = Path.joinpath(self._cache_path, file_name)
        try:
            with shelve.open(path_to_file.__str__()) as cache_file:
                cache_file[key] = data
        except:
            # logger here
            return False

        return True


    def get_cache(self, cache_name, key: Optional[str]=None) -> ProxyInfo | None:
        """Returns cache using a key or the first item of the cached data"""
        if not key:
            keys = self.get_cache_keys(cache_name)
            if keys:
                key = keys[0]

        file_name = cache_name
        path_to_file = Path.joinpath(self._cache_path, file_name)

        cached_data = None
        try:
            with shelve.open(path_to_file.__str__()) as cache_file:
                cached_data = cache_file[key]
        except KeyError as er:
            # logger or something
            pass

        return cached_data

    def get_all_cache(self, cache_name: str) -> List[ProxyInfo]| None:

        keys = self.get_cache_keys(cache_name)
        if not keys:
            return None

        file_name = cache_name
        path_to_file = Path.joinpath(self._cache_path, file_name)

        cache = []
        try:
            with shelve.open(path_to_file.__str__()) as cache_file:
                for key in keys:
                    cache.append(cache_file[key])
        except:
            # logger or something
            pass

        return cache



    def write_valid_proxy(self, data):

        today = format_date(date.today())
        file_name = f'valid_{today}'
        print(data)
        key = data.country.upper()
        if len(key) > 2:
            key = country_code(key)
            
        path_to_file = Path.joinpath(self._cache_path, file_name)
        try:
            with shelve.open(path_to_file.__str__()) as cache_file:
                key_items = cache_file.get(key, [])
                key_items.append(data)
                cache_file[key] = key_items
        except:
            # logger here
            return False

        return True


    def get_cache_names(self) -> List:
        """Returns cache names in a list"""
        names = []
        paths = list(self._cache_path.iterdir())
        for path in paths:
            if path.is_file():
                names.append(path.name)

        return names

    def get_cache_keys(self, db_name) -> List:
        """Returns all the keys from a cache_name"""
        file_name = db_name
        path_to_file = Path.joinpath(self._cache_path, file_name)

        keys = []
        try:
            with shelve.open(path_to_file.__str__()) as cache_file:
                keys = list(cache_file.keys())
        except:
            pass

        return keys

    def delete_cache(self, key: str) -> bool:
        """Deletes 1 cache item using a key"""
        pass

    def delete_all_cache(self) -> bool:
        """Deletes all cached items"""
        pass
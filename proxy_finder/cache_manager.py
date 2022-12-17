import shelve
from typing import List

from proxy_finder.abstract import ProxyInfo

def write_cache(data) -> bool:
    """Write the cache, returns true if successful"""
    pass


def get_cache(key) -> ProxyInfo:
    """Returns cache using a key"""
    pass

def get_cache_names(key) -> List:
    """Returns cache names in a list"""
    pass

def delete_cache(key: str) -> bool:
    """Deletes 1 cache item using a key"""
    pass

def delete_all_cache() -> bool:
    """Deletes all cached items"""
    pass
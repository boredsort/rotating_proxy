import random
from datetime import date
from typing import List

from proxy_finder.abstract import ProxyInfo
from proxy_finder.cache_manager import CacheManager
from proxy_finder.proxy_finder import ProxyFinder
import proxy_finder.utils.formatter as format
# this should contain proxy_manager class
    # should find proxy
    # should cache the proxy
    # should manage caches and clean up
    # should have exhaustive find proxy
    # should have a method to be used by the requester to get proxies by a specific countries

class ProxyManager:

    def __init__(self):

        self._cache_manager = CacheManager()
        today = date.today()
        self._cache_name = format.format_date(today) 

    def find_proxies(self, sites: str | List[str], force: bool = False) -> List[ProxyInfo | None]:
        """Returns a list of proxies from a site or cache"""

        # try refactoring this code later to be multithreaded for faster proxy finder extraction

        if isinstance(sites, str):
            tmp = sites
            sites = []
            sites.append(tmp)
            
        proxies = []

        for site in sites:

            # cached_list = cache_manager.get_cache_names()
            site_key = format.format_sitename(site)
            cached = None
            if not force:
                cached = self._cache_manager.get_cache(self._cache_name, site_key)

            if cached:
                proxies.append(cached)
            else:
                # extract proxy from site
                # write to cache
                proxy_finder = ProxyFinder()
                proxy_info = proxy_finder.extract(site)
                success = self._cache_manager.write_cache(proxy_info)
                if success:
                    # log info success cache writing
                    pass
                else:
                    pass
                    # logger info error writing to cache

                proxies.append(proxy_info)

        return proxies

    def get_proxy(self, **params):
        """Returns a proxy using a specific paramater i.e. country or protocol
           Default param is a random country
        """

        # For future update, if there are no specific country, proxy finder should find proxies on other sites

        cached = self._cache_manager.get_cache(self._cache_name)
        if cached:
            pass
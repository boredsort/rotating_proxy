import random
from datetime import date

from typing import List

from proxy_finder.abstract import ProxyInfo, ProxyData
from proxy_finder.cache_manager import CacheManager
from proxy_finder.proxy_finder import ProxyFinder
import proxy_finder.utils.formatter as format
from pycountry import countries

# def find_proxies(sites: str | List[str], force: bool = False) -> List[ProxyInfo | None]:
#     """Returns a list of proxies from a site or cache"""

#     # try refactoring this code later to be multithreaded for faster proxy finder extraction

#     if isinstance(sites, str):
#         tmp = sites
#         sites = []
#         sites.append(tmp)
        
#     proxies = []

#     today = date.today()
#     cache_name = format.format_date(today) 
#     for site in sites:
#         cache_manager = CacheManager()
#         # cached_list = cache_manager.get_cache_names()
#         site_key = format.format_sitename(site)
#         cached = None
#         if not force:
#             cached = cache_manager.get_cache(cache_name, site_key)

#         if cached:
#             proxies.append(cached)
#         else:
#             # extract proxy from site
#             # write to cache
#             proxy_finder = ProxyFinder()
#             proxy_info = proxy_finder.extract(site)
#             success = cache_manager.write_cache(proxy_info)
#             if success:
#                 # log info success cache writing
#                 pass
#             else:
#                 pass
#                 # logger info error writing to cache

#             proxies.append(proxy_info)

#     return proxies

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
        country_code = params.get('country', None)

        cached = self._cache_manager.get_cache(self._cache_name)

        if cached:
            proxies = self._find_proxy_by_country(country_code, cached.proxy_list)
            if proxies:
                return random.choice(proxies)
            else:
                # returns Just random country if nothing found
                proxies = cached.proxy_list
                return random.choice(proxies)

        return None


    def _find_proxy_by_country(self, country_code, proxy_list) -> list[ProxyData]:
        
        country = self._country_name(country_code)

        found = []

        if proxy_list:
            found = filter(lambda cn: cn.country.lower() in country.name.lower(), proxy_list)
        
        return list(found)



    @staticmethod
    def _sort_proxies(proxies_list: List) -> List:

        def get_country(element):
            return element.country.lower()

        proxies = sorted(proxies_list, key=get_country)

        return proxies
        
    
    @staticmethod
    def _country_name(code: str) -> str:
        return countries.get(alpha_2=code)
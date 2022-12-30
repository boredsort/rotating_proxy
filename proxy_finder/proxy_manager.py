import random
from datetime import date

from typing import List

from proxy_finder.abstract import ProxyInfo, ProxyData
from proxy_finder.cache_manager import CacheManager
from proxy_finder.proxy_finder import ProxyFinder
import proxy_finder.utils.formatter as format
from pycountry import countries

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

        cached = self._cache_manager.get_all_cache(self._cache_name)

        found_proxies = []

        if cached:

            for item in cached:
                found_proxies.extend(self._find_proxy_by_country(country_code, item.proxy_list))

            if found_proxies:
                return random.choice(found_proxies)
            else:
                # returns Just random country if nothing found
                proxies = random.choice(cached)
                return random.choice(proxies.proxy_list)

        return None


    def _find_proxy_by_country(self, country_code, proxy_list) -> list[ProxyData]:
        
        country = self._country_name(country_code)

        found = []

        if country:
            def get_country(element):

                proxy_country = element.country.lower()
                request_country = country.name.lower()
                if len(proxy_country) == 2:
                    request_country = country.alpha_2.lower()

                if request_country in proxy_country:
                    return True
                else:
                    return False


            if proxy_list:
                found = filter(get_country, proxy_list)
        
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
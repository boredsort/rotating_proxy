import random
import threading
from collections import deque
from datetime import date
from typing import List, Dict

import requests
from fake_useragent import UserAgent

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
        self.queue = None

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
                cached = self._cache_manager.get_cache(
                    self._cache_name, site_key)

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

    def get_proxy(self, **params) -> Dict:
        """Returns a proxy using a specific paramater i.e. country or protocol
           Default param is a random country
        """
        # should return a dictionary of a http and https

        # For future update, if there are no specific country, proxy finder should find proxies on other sites
        country_code = params.get('country', None)

        cached = self._cache_manager.get_all_cache(self._cache_name)

        found_proxies = []

        proxy = {}

        if cached:

            for item in cached:
                found_proxies.extend(self._find_proxy_by_country(
                    country_code, item.proxy_list))

            if found_proxies:
                found_proxy = random.choice(found_proxies)
                protocols = found_proxy.protocols
                for p in protocols:
                    url = f'{p.lower()}://{found_proxy.ip}:{found_proxy.port}'
                    if 'socks4' in p or 'socks5' in p:
                        proxy.update({
                            'http': url,
                            'https': url,
                        })
                    else:
                        proxy.update({
                            p.lower(): url
                        })

                # what is missing, if http or https
                missing = None
                p_list = ['http', 'https']
                for p in p_list:
                    if p not in proxy:
                        missing = p

                # if there is missing, find a the missing
                if missing:
                    found_missing = self._get_proxyby_protocol(
                        missing, found_proxies)
                    if found_missing:
                        protocols = found_missing.protocols
                        for p in protocols:
                            url = f'{p.lower()}://{found_missing.ip}:{found_missing.port}'
                            if missing == p.lower():
                                proxy.update({p.lower(): url})

                    else:
                        # if cannot find use socks4 or socks5
                        found_missing = self._get_proxyby_protocol(
                            'socks4', found_proxies)
                        if found_missing:
                            protocols = found_missing.protocols
                            for p in protocols:
                                url = f'{p.lower()}://{found_missing.ip}:{found_missing.port}'
                                if missing == p.lower():
                                    proxy.update({p.lower(): url})

            else:
                # returns Just random country if nothing found
                proxies = random.choice(cached)
                return random.choice(proxies.proxy_list)

        return proxy

    def _validate_proxy(self, proxy_queue: deque) -> None:


        def _requests(proxy):
            ua = UserAgent()
            test_sites = ['https://api.myip.com/', 'https://ipinfo.io/json', 'https://ifconfig.me/']
            headers = {"User-Agent": ua.random,
                        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
            }
            proxies = {
                'http': f'{proxy.protocol}://{proxy.ip}:{proxy.port}',
                'https': f'{proxy.protocol}://{proxy.ip}:{proxy.port}'
            }

            try:
                response = requests.get(random.choice(test_sites), heaeders=headers, proxies=proxies)
                if response.status_code in [200, 201]:
                    return {'alive': True, 'proxy': proxy }

            except:
                pass
            return {'alive': False, 'proxy': proxy }

        pass
           
        while self.queue:
            proxy = self.queue.pop()
            result = _requests(proxy)


        pass

    def validate_proxies(self, cache_name):
        """Takes cached proxy and validates the found proxy if it is still valid.

        Args:
            cache_name (str, optional): is string date e.g 2022_10_20, if param is provided
            default is the current date
        """
        if not cache_name:   
            cache_name = self._cache_name

        proxies_list = self._cache_manager.get_all_cache(cache_name)
        if proxies_list:
            deq = deque(proxies_list)

            # for _ range(6):
            #     threading.Thread(target=)

                

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

    def _get_proxyby_protocol(self, protocol, proxy_list):

        found = None
        for proxy in proxy_list:
            protocols = proxy.protocols
            for p in protocols:
                if p.lower() == protocol.lower():
                    found = proxy
                    break

        return found

    @staticmethod
    def _sort_proxies(proxies_list: List) -> List:

        def get_country(element):
            return element.country.lower()

        proxies = sorted(proxies_list, key=get_country)

        return proxies

    @staticmethod
    def _country_name(code: str) -> str:
        return countries.get(alpha_2=code)

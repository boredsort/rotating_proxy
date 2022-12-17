
from typing import List

from proxy_finder.abstract import ProxyInfo
from proxy_finder.cache_manager import get_cache_names, get_cache, write_cache
from proxy_finder.proxy_finder import ProxyFinder

def find_proxies(sites: str | List[str]) -> List[ProxyInfo | None]:
    """Returns a list of proxies from a site or cache"""

    # check if items in site exist in cache
        # if now then get from the website


    # try refactoring this code later to be multithreaded for faster proxy finder extraction

    proxies = []
    # temporary, will be updated
    date = '_2022_12_17'
    for site in sites:
        cached_list = get_cache_names()
        
        site_key = site + date
        if site_key in cached_list:
            cached_proxy = get_cache(site_key)
            proxies.append(cached_proxy)
        else:
            # extract proxy from site
            # write to cache
            proxy_finder = ProxyFinder()
            proxy_info = proxy_finder.extract(site)
            success = write_cache(proxy_info)
            if success:
                # log info success cache writing
                pass
            else:
                pass
                # logger info error writing to cache

            proxies.append(proxy_info)

    return proxies

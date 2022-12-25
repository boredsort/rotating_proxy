from datetime import date

from typing import List

from proxy_finder.abstract import ProxyInfo
from proxy_finder.cache_manager import CacheManager
from proxy_finder.proxy_finder import ProxyFinder
import proxy_finder.utils.formatter as format

def find_proxies(sites: str | List[str], force: bool = False) -> List[ProxyInfo | None]:
    """Returns a list of proxies from a site or cache"""

    # try refactoring this code later to be multithreaded for faster proxy finder extraction

    if isinstance(sites, str):
        tmp = sites
        sites = []
        sites.append(tmp)
        
    proxies = []

    today = date.today()
    cache_name = format.format_date(today) 
    for site in sites:
        cache_manager = CacheManager()
        # cached_list = cache_manager.get_cache_names()
        site_key = format.format_sitename(site)
        cached = None
        if not force:
            cached = cache_manager.get_cache(cache_name, site_key)

        if cached:
            proxies.append(cached)
        else:
            # extract proxy from site
            # write to cache
            proxy_finder = ProxyFinder()
            proxy_info = proxy_finder.extract(site)
            success = cache_manager.write_cache(proxy_info)
            if success:
                # log info success cache writing
                pass
            else:
                pass
                # logger info error writing to cache

            proxies.append(proxy_info)

    return proxies

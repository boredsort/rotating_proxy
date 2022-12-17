
from typing import List

from proxy_finder.abstract import ProxyInfo

def find_proxies(sites: str | List[str]) -> List[ProxyInfo | None]:
    """Returns a list of proxies from a site or cache"""
    
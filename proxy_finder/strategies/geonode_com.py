import json
import re
from datetime import datetime

import requests
from fake_useragent import UserAgent

from proxy_finder.abstract import ProxyData, ProxyInfo
from proxy_finder.base import BaseStrategy
from proxy_finder.utils.decorators import attribute
from proxy_finder.utils.decoder import UtfJS


class GeonodeComStrategy(BaseStrategy):

    URL = 'https://geonode.com/'

    def execute(self) -> ProxyInfo:
        
        raw = self.download(self.URL)
        proxy_info = self.parse(raw)

        return proxy_info

    def download(self, url: str) -> str:

        api_url = 'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc'
        raw: str = None
        ua = UserAgent()

        headers = {
            'User-Agent': ua.random,
            "accept": "application/json",
            "accept-encoding": "gzip, deflate",
            "accept-language": "en-US,en;q=0.9",
            "origin": "https://geonode.com",
            "referer": "https://geonode.com/"
        }

        try:
            response = requests.get(api_url, headers=headers)

            if response.status_code in [200, 201]:
                response.encoding = 'UTF-8'

                raw = response.text

        except:
            raw = None

        return raw

    def parse(self, raw: str) -> ProxyInfo:

        proxy_info = ProxyInfo()
        proxy_info.meta.source_url = self.URL
        
        try:
            _json = json.loads(raw)
            if _json and 'data' in _json:
                items = _json.get('data', None)
                proxy_list = []
                if items:
                    for item in items:
                        proxy = ProxyData()
                        proxy.ip = self.get_ip_add(item)
                        proxy.port = self.get_port_number(item)
                        proxy.protocols = self.get_protocols(item)
                        proxy.anonymity = self.get_anonimity(item)
                        proxy.country = self.get_country(item)
                        proxy.region = self.get_region(item)
                        proxy.city = self.get_city(item)
                        proxy.uptime = self.get_uptime(item)
                        try:
                            if proxy.validate():
                                proxy_list.append(proxy)
                        except:
                            # should have a logger here
                            continue

                        proxy_info.proxy_list = proxy_list
        except:
            pass

        return proxy_info

    @attribute
    def get_ip_add(self, item):
        return item.get('ip', None)

    @attribute
    def get_port_number(self, item):
        return int(item.get('port', None))

    @attribute
    def get_protocols(self, item):
        return item.get('protocols', [])

    @attribute
    def get_anonimity(self, item):
        return item.get('anonymityLevel', None)
    
    @attribute
    def get_country(self, item):
        return item.get('country', None)
    
    @attribute
    def get_city(self, item):
        return item.get('city', None)

    @attribute
    def get_region(self, item):
        return item.get('region', None)

    @attribute
    def get_uptime(self, item):
        return item.get('upTime', None)
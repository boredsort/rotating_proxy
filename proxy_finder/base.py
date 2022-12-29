import json

import requests
from fake_useragent import UserAgent

from proxy_finder.abstract import AbstractStrategy
from proxy_finder.abstract import ProxyData, ProxyInfo

class BaseStrategy(AbstractStrategy):

    def execute(self)->ProxyInfo:
        
        raw = self.download(self.URL)
        proxy_info = self.parse(raw)

        return proxy_info

    def download(self, url:str)->str:

        raw:str = None
        ua = UserAgent()

        headers = {
            'User-Agent': ua.random
        }
       
        try:
            response = requests.get(url, headers=headers)

            if response.status_code in [200, 201]:
                response.encoding = 'UTF-8'

                raw = response.text

        except:
            raw = None

        return raw

    def parse(self, raw:str)->json:
        pass
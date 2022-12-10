import json

import requests
from fake_useragent import UserAgent

from proxy_finder.abstract import AbstractStrategy

class BaseStrategy(AbstractStrategy):

    def execute(self, url:str)->list:
        
        raw = self.download(url)
        _json = self.parse(raw)

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
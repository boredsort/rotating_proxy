import json

import requests
import cloudscraper
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from proxy_finder.base import BaseStrategy, ResultData


class FreeProxyListsNetStrategy(BaseStrategy):


    def __init__(self):
        self.scraper = cloudscraper.create_scraper()

    def execute(self, url:str)->ResultData:
        
        raw = self.download(url)
        _json = self.parse(raw)

    def download(self, url:str)->str:

        raw:str = None
        ua = UserAgent()

        headers = {
            'User-Agent': ua.random,
            "origin": "https://www.freeproxylists.net",
            "referer": "https://www.freeproxylists.net/",
            "accept-encoding": "gzip, deflate",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "max-age=0"
        }
       
        try:
            response = self.scraper.get(url, headers=headers)

            if response.status_code in [200, 201]:
                response.encoding = 'UTF-8'

                raw = response.text

        except:
            raw = None

        return raw

    def parse(self, raw:str)->json:
        soup = BeautifulSoup(raw, 'lxml')

        data_grid_tag = soup.body.select_one('.DataGrid')

    def get_ip_add(self, soup):
        pass
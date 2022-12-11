import json
import re
from datetime import datetime

import requests
import cloudscraper
from bs4 import BeautifulSoup, Tag
from fake_useragent import UserAgent

from proxy_finder.abstract import ProxyData, ProxyInfo
from proxy_finder.base import BaseStrategy
from proxy_finder.utils.decorators import attribute
from proxy_finder.utils.decoder import UtfJS


class FreeproxylistsNetStrategy(BaseStrategy):

    URL = 'https://www.freeproxylists.net/'

    def __init__(self):
        self.scraper = cloudscraper.create_scraper()

    def execute(self) -> ProxyInfo:

        raw = self.download(self.URL)
        _json = self.parse(raw)


    def download(self, url: str) -> str:

        raw: str = None
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

    def parse(self, raw: str) -> json:
        soup = BeautifulSoup(raw, 'lxml')

        proxy_list = []

        data_grid_tag = soup.body.select_one('.DataGrid')

        if not data_grid_tag:
            # should have an error logger here
            # message should be blocked or not grid found
            return proxy_list

        row_tags = data_grid_tag.select('tr:not(.Caption)')
        if row_tags:

            for row in row_tags:
                # filter ads
                if not row.select_one('[src*=pagead]'):
                    proxy = ProxyData()
                    proxy.ip = self.get_ip_add(row)
                    proxy.port = self.get_port_number(row)
                    proxy.protocol = self.get_protocol(row)
                    proxy.anonymity = self.get_anonimity(row)
                    proxy.country = self.get_country(row)
                    proxy.region = self.get_region(row)
                    proxy.city = self.get_city(row)
                    proxy.uptime = self.get_uptime(row)
                    try:
                        if proxy.validate():
                            proxy_list.append(proxy)
                    except:
                        # should have a logger here
                        continue

        proxy_info = ProxyInfo()
        proxy_info.proxy_list = proxy_list
        proxy_info.meta.extraction_date = datetime().now()
        proxy_info.meta.source_url = self.URL
        
        return proxy_list

    @attribute
    def get_ip_add(self, row_tag: Tag) -> str:
        value = None
        tag = row_tag.select_one('td:nth-child(1)')
        if tag:
            utf = UtfJS()
            txt = tag.script.get_text().strip().strip('IPDecode("').strip('")')
            decoded = utf.decode(txt)
            inner_txt = re.sub(r'<.*?>', ' ', decoded)
            value = ''.join(re.findall(r'([0-9|.]+)', inner_txt))

        return value

    @attribute
    def get_port_number(self, row_tag: Tag) -> int:
        value = None
        tag = row_tag.select_one('td:nth-child(2)')
        if tag:
            value = int(tag.get_text().strip())

        return value

    @attribute
    def get_protocol(self, row_tag: Tag) -> str:
        value = None
        tag = row_tag.select_one('td:nth-child(3)')
        if tag:
            value = tag.get_text().strip()

        return value

    @attribute
    def get_anonimity(self, row_tag: Tag) -> str:
        value = None
        tag = row_tag.select_one('td:nth-child(4)')
        if tag:
            value = tag.get_text().strip()

        return value

    @attribute
    def get_country(self, row_tag: Tag) -> str:
        value = None
        tag = row_tag.select_one('td:nth-child(5)')
        if tag:
            value = tag.get_text().strip()

        return value

    @attribute
    def get_region(self, row_tag: Tag) -> str:
        value = None
        tag = row_tag.select_one('td:nth-child(6)')
        if tag:
            value = tag.get_text().strip()

        return value

    @attribute
    def get_city(self, row_tag: Tag) -> str:
        value = None
        tag = row_tag.select_one('td:nth-child(7)')
        if tag:
            value = tag.get_text().strip()

        return value

    @attribute
    def get_uptime(self, row_tag: Tag) -> str:
        value = None
        tag = row_tag.select_one('td:nth-child(8)')
        if tag:
            value = tag.get_text().strip()

        return value

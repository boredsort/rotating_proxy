import json

from fake_useragent import UserAgent

from proxy_finder.base import BaseStrategy, ResultData


class FreeProxyListsNetStrategy(BaseStrategy):

    def execute(self, url:str)->ResultData:
        
        raw = self.download(url)

    def download(self, url:str)->str:
        pass

    def parse(self, raw:str)->json:
        pass
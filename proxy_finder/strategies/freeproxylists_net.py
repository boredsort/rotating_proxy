from proxy_finder.abstract import AbstractStrategy


class FreeProxyListsNetStrategy(AbstractStrategy):

    def execute(self, url:str) -> str:
        pass

    def download(self, url:str)->str:
        pass
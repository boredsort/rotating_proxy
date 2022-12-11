import json
from typing import List
from pathlib import Path, PosixPath

from proxy_finder.abstract import ProxyInfo
from proxy_finder.factory import StrategyFactory


class ProxyFinder:

    def extract(self, site: str) -> ProxyInfo:
        
        strategy = StrategyFactory().get_strategy(site)()

        proxy_info = strategy.execute()

        return proxy_info


    def extract_all(self) -> List[ProxyInfo]:

        base_dir = Path.cwd()
        sites_map_path = Path.joinpath(base_dir, PosixPath('proxy_finder/map.json')) 
        sites_json = None

        with sites_map_path.open('r') as site_map:
            text = site_map.read()
            sites_json = json.loads(text)

        list_proxy_info = []
        if sites_json:
            for site in sites_json:
                proxy_info = self.extract(site)
                list_proxy_info.append(proxy_info)

        return list_proxy_info


from pathlib import Path, PosixPath
import json
import importlib


class StrategyFactory:

    SITES_MAP_FILE = 'map.json'
    MAP = {}

    def __init__(self):

        base_dir = Path.cwd()
        file_path = PosixPath('proxy_finder/' + self.SITES_MAP_FILE)
        file = Path.joinpath(base_dir, file_path)

        try:
            with file.open('r') as map_file:
                text = map_file.read()
                self.MAP = json.loads(text)
        except FileNotFoundError as e:
            # will be updated when the logger is built
            print(e.strerror + e.filename )
        except:
            raise Exception("Failed to create factory object")

    def get_strategy(self, site: str):
        
        site = site.lower()
        if 'www.' in site:
            site = site.replace('www.','')

        file_name = self.MAP[site]
        module_path = f'proxy_finder.strategies.{file_name}'
        module = importlib.import_module(module_path)
        class_name = f'{self._get_class_name(file_name)}Strategy'
        return getattr(module, class_name)
        
    @staticmethod
    def _get_class_name(file_name):
        if not file_name:
            return None

        file_name = file_name.lower()
        splited_name = file_name.split('_')

        class_name = ''
        for word in splited_name:
            class_name += word.capitalize()

        return class_name
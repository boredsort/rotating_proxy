from pathlib import Path, PosixPath
import json
import importlib


class StrategyFactory:

    SITES_MAP_FILE = 'map.json'
    MAP = {}

    def __init__(self):

        base_dir = Path.cwd()
        file_path = PosixPath(self.SITES_MAP_FILE)
        file = Path.joinpath(base_dir, file_path)

        try:
            with file.open('r') as map_file:
                self.MAP = json.loads(map_file)
        except FileNotFoundError as e:
            # will be updated when the logger is built
            print(e.strerror + e.filename )
        except:
            raise Exception("Failed to create factory object")

    def get_strategies(self):
        pass


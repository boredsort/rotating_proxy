import json
from datetime import date
from pathlib import Path

import shelve


from proxy_finder.cache_manager import CacheManager
from proxy_finder.abstract import ProxyInfo
import proxy_finder.utils.formatter as format

def test_write_cache():
    cache_manager = CacheManager()
    proxy_info = ProxyInfo()
    proxy_info.meta.source_url = 'www.freeproxylist.net'
    proxy_info.proxy_list = []
    # data = json.loads(json.dumps({
    #     'meta': {
    #         'source_url': 'www.freeproxylist.net'
    #     },
    #     'data': 'sample'
    # }),
    # object_hook=ProxyInfo
    # )

    success = cache_manager.write_cache(proxy_info)

    today = format.format_date(date.today())
    temp_path = Path('./proxy_finder/temp')
    cache_path = Path.joinpath(Path.cwd(), temp_path)
    cache_path.mkdir(exist_ok=True)

    file_name = format.format_sitename(proxy_info.meta.source_url)
    path_to_file = Path.joinpath(cache_path, file_name)
    cached_data = None
    with shelve.open(path_to_file.__str__()) as cache_file:
        cached_data = cache_file[today]

    assert cached_data.meta.source_url == proxy_info.meta.source_url
    assert success == True


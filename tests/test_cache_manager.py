import json
from datetime import date
from pathlib import Path

import shelve

from proxy_finder.cache_manager import CacheManager
from proxy_finder.abstract import ProxyInfo, ProxyData
import proxy_finder.utils.formatter as format


def test_write_cache():
    cache_manager = CacheManager()
    proxy_info = ProxyInfo()
    proxy_info.meta.source_url = 'www.freeproxylist.net'
    proxy_info.proxy_list = []

    success = cache_manager.write_cache(proxy_info)

    today = format.format_date(date.today())
    temp_path = Path('./proxy_finder/temp')
    cache_path = Path.joinpath(Path.cwd(), temp_path)
    cache_path.mkdir(exist_ok=True)

    key = format.format_sitename(proxy_info.meta.source_url)
    path_to_file = Path.joinpath(cache_path, today)
    cached_data = None
    with shelve.open(path_to_file.__str__()) as cache_file:
        cached_data = cache_file[key]

    assert cached_data.meta.source_url == proxy_info.meta.source_url
    assert success == True

def test_get_cache():
    cache_manager = CacheManager()
    proxy_info = ProxyInfo()
    proxy_info.meta.source_url = 'www.freeproxylist.net'
    proxy_info.proxy_list = []

    success = cache_manager.write_cache(proxy_info)
    key = format.format_sitename(proxy_info.meta.source_url)
    today = format.format_date(date.today())
    cached_data = cache_manager.get_cache(today, key)

    assert cached_data.meta.source_url == proxy_info.meta.source_url
    assert success == True

def test_write_valid_proxy():
    valid = ProxyData()
    valid_2 = ProxyData()

    # this is stupid code
    valid.ip='64.124.191.98'
    valid.port=32688
    valid.country='US'
    valid.protocols=['socks4']
    valid.region='NOT_FOUND'
    valid.city='Conshohocken'
    valid.anonymity='elite'
    valid.uptime='100'

    valid.ip='64.124.191.100'
    valid.port=32688
    valid.country='US'
    valid.protocols=['socks4']
    valid.region='NOT_FOUND'
    valid.city='Conshohocken'
    valid.anonymity='elite'
    valid.uptime='100'

    cache_manager = CacheManager()
    cache_manager.write_valid_proxy(valid)
    cache_manager.write_valid_proxy(valid_2)


    cached_data = cache_manager.get_cache('valid_2023_01_13', 'US')

    assert len(cached_data) == 2
    # assert valid in cached_data



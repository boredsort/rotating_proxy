import pytest

import proxy_finder.utils.formatter as format


def test_sitename_formatter():
    https_www_url = 'https://www.freeproxylists.net/'
    http_www_url = 'https://www.freeproxylists.net/'

    correct_value = 'freeproxylists.net'
    assert format.format_sitename(https_www_url) == correct_value
    assert format.format_sitename(http_www_url) == correct_value
    assert format.format_sitename(http_www_url.upper()) == correct_value
    assert format.format_sitename(None) == None

def test_format_date():
    
    from datetime import date

    da = date(2022, 12, 19)

    assert format.format_date(da) == '2022_12_19'



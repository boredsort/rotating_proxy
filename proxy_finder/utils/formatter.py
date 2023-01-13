from datetime import date
from pycountry import countries


def format_sitename(url: str) -> str:

    if not url:
        return None

    return url.lower().replace('http://', '').replace('https://', '').replace('www.', '').strip('/')


def format_date(date: date):

    return date.strftime('%Y_%m_%d')


def country_code(name: str) -> str:
    return countries.get(name=name).alpha_2

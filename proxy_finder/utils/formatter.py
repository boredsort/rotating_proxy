from datetime import date

def format_sitename(url: str) -> str:

    if not url:
        return None

    return url.lower().replace('http://', '').replace('https://', '').replace('www.','').strip('/')


def format_date(date: date):

    return date.strftime('%Y_%m_%d')
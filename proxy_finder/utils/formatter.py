
def format_sitename(url: str):

    if not url:
        return None

    url = url.replace('http://', '').replace('https://', '').replace('www.','')
    return url
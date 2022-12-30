

from proxy_finder.proxy_manager import ProxyManager

from .base import BaseProxyRequest


class ProxyRequest(BaseProxyRequest):

    def __init__(self, country_code, retries=5, backoff_factor=5, status_forcelist=None):

        proxy_manager = ProxyManager()
        proxy = proxy_manager.get_proxy(country=country_code)

        super().__init__(retries=retries, backoff_factor=backoff_factor, status_forcelist=status_forcelist,
                         proxies=proxy)

        proxy_info = self._get_proxy_connection_info()

        
        if not proxy_info or (isinstance(proxy_info, str) and 'error' in proxy_info.lower()):
            # raise Exception('Proxy Error. Reason: Unhandled exception.')
            print('Proxy Info. Reason: Unable to retrieve proxy info.')
            proxy_info = None

        self.proxy_info = proxy_info

    def get(self, url, timeout=10, headers=None, cookies=None, verify=False, stream=False):
        if isinstance(headers, type(None)):
            headers = {}

        if isinstance(cookies, type(None)):
            cookies = {}


        return self.session.get(url, timeout=timeout, headers=headers, cookies=cookies, verify=verify, stream=False)

    def post(self, url, timeout=10, data=None, headers=None, cookies=None, verify=False):
        if isinstance(headers, type(None)):
            headers = {}

        if isinstance(cookies, type(None)):
            cookies = {}


        return self.session.post(url, data=data, timeout=timeout, headers=headers, cookies=cookies, verify=verify)

    def put(self, url, timeout=10, data=None, headers=None, cookies=None, verify=False):
        if isinstance(headers, type(None)):
            headers = {}

        if isinstance(cookies, type(None)):
            cookies = {}

        return self.session.put(url, data=data, timeout=timeout, headers=headers, cookies=cookies, verify=verify)

    
    def _get_proxy_connection_info(self):
        print('Get info from proxy: %s' % self.proxies['http'])
        try:
            res = self.session.get('https://ipinfo.io/json', verify=False)

            if res.status_code == 200:
                return res.text

            return False

        except:
            return False

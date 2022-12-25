from urllib3.util import Retry

import requests
from requests.adapters import HTTPAdapter


class ProxyRequest:

    def __init__(self, retries=5, backoff_factor=5, status_forcelist=None, proxies=None):

        self.retries = retries
        self.backoff_factor = backoff_factor
        self.status_forcelist = status_forcelist
        self.proxies = proxies

        # write a ProxyManager instance here to get the proxies

        self.session = self._create_requests_session(retries, backoff_factor=backoff_factor,
                                                     status_forcelist=status_forcelist, proxies=proxies)

  
    def get(self, url, timeout=10, headers={}, verify=False):
        raise NotImplementedError


    def post(self, url, timeout=10, data=None, headers=None, verify=False):
        raise NotImplementedError


    def put(self, url, timeout=10, data=None, headers=None, verify=False):
        raise NotImplementedError

    @staticmethod
    def _create_requests_session(retries, backoff_factor, status_forcelist, proxies):
        session = requests.Session()

        if proxies:
            session.proxies.update(proxies)

        retry = Retry(total=retries, read=retries, connect=retries, backoff_factor=backoff_factor, 
                        status_forcelist=status_forcelist)

        adapter= HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter) 

        return session
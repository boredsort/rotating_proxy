from abc import ABCMeta, abstractmethod
from datetime import datetime
import json

from schema import Optional

from proxy_finder.result_validator import validate as _validate


class AbstractStrategy(metaclass=ABCMeta):

    @abstractmethod
    def execute(self, url:str)->'ProxyInfo':
        raise NotImplementedError

class MetaData:

    source_url:str
    extraction_date:datetime

class ProxyData:

    ip: str
    port: int
    country: str
    protocol: str
    region: Optional(str)
    city: Optional(str)
    anonymity: Optional(str)
    uptime: Optional(str)

class ProxyInfo:

    meta: MetaData
    data: ProxyData

    def validate(self):
        return _validate(self)


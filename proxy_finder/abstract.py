from abc import ABCMeta, abstractmethod
from datetime import datetime
import json
from dataclasses import dataclass

from schema import Optional

from proxy_finder.result_validator import validate as _validate


class AbstractStrategy(metaclass=ABCMeta):

    @abstractmethod
    def execute(self) -> 'ProxyInfo':
        raise NotImplementedError
@dataclass
class MetaData:

    source_url: str
    extraction_date: datetime

    def __init__(self):

        self.extraction_date = datetime.now()

@dataclass
class ProxyData():

    ip: str
    port: int
    country: str
    protocol: str
    region: Optional(str)
    city: Optional(str)
    anonymity: Optional(str)
    uptime: Optional(str)

    def __init__(self):
        super().__init__()

    def validate(self):
        return _validate(self.__dict__)

@dataclass
class ProxyInfo:

    meta: MetaData
    proxy_list: list[ProxyData]

    def __init__(self):

        self.meta = MetaData()




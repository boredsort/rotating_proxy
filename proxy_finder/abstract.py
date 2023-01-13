from abc import ABCMeta, abstractmethod
from datetime import datetime
import json
from dataclasses import dataclass, field

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


@dataclass(order=True)
class ProxyData:

    ip: str
    port: int
    country: str
    protocols: list
    region: Optional(str)
    city: Optional(str)
    anonymity: Optional(str)
    uptime: Optional(str)

    def __init__(self):
        self.ip='0',
        self.port=0
        self.country='NA'
        self.protocols=[],
        self.region='None'
        self.city='None'
        self.anonymity='None'
        self.uptime='0'
        super().__init__()

    def validate(self):
        return _validate(self.__dict__)


@dataclass
class ProxyInfo:

    meta: MetaData
    proxy_list: list[ProxyData]

    def __init__(self):

        self.meta = MetaData()
        self.proxy_list = field(default_factory=list)

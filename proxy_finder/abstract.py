from abc import ABCMeta, abstractmethod
import json

class AbstractStrategy(metaclass=ABCMeta):

    @abstractmethod
    def execute(self, url:str)->json:
        raise NotImplementedError


class ResultData:

    pass
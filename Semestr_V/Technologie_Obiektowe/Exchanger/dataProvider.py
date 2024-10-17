from abc import ABC, abstractmethod
import requests

class IDataProvider(ABC):
    @abstractmethod
    def getData(self, data: str):
        pass
    
    @abstractmethod
    def getInstance(self):
        pass

class DataProvider(IDataProvider):
    
    def __init__(self):
        self.provider = None
        self.url = "https://api.nbp.pl/api/exchangerates/tables/a/"

    def getData(self, data: str):
        return requests.get(self.url)

    @staticmethod
    def getInstance():
        pass
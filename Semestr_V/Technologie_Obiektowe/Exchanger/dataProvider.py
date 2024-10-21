from abc import ABC, abstractmethod
import requests

class IDataProvider(ABC):
    @abstractmethod
    def getData(self):
        pass
    
    @abstractmethod
    def getInstance(self):
        pass

class DataProvider(IDataProvider):
    
    def __init__(self):
        self.url = "https://api.nbp.pl/api/exchangerates/tables/a/"

    def getData(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f'Error while loading data: {e}')
            return None

    @staticmethod
    def getInstance():
        return DataProvider()
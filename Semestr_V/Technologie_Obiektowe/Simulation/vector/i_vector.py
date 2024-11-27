from abc import ABC, abstractmethod

class IVector(ABC):
    @staticmethod
    @abstractmethod
    def abs(self) -> float:
        pass
    
    @staticmethod
    @abstractmethod
    def cdot(self, other) -> float:
        pass
    
    @staticmethod
    @abstractmethod
    def get_components(self) -> list[float]:
        pass
    
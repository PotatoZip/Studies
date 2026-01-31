from abc import ABC, abstractmethod
from typing import List
import math

class IVector(ABC):
    @abstractmethod
    def abs(self) -> float:
        pass
    @abstractmethod
    def cdot(self, vector: 'IVector') -> float:
        pass

    @abstractmethod
    def getComponents(self) -> List[float]:
        pass
    
class Vector2D(IVector):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def abs(self) -> float:
        return math.sqrt((self.x*self.x) + (self.y*self.y))

    def cdot(self, vector: 'Vector2D') -> float:
        return self.getX()*vector.getX() + self.getY()*vector.getY()

    def getComponents(self) -> list[float]:
        return [self.x, self.y]
    
    def getX(self) -> float:
        return self.x
    
    def getY(self) -> float:
        return self.y

    

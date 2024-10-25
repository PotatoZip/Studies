from abc import ABC, abstractmethod
from vector2D import IVector, Vector2D
from typing import List
from math import atan2, degrees

class IPolar2D(ABC):
    @abstractmethod
    def abs(self) -> float:
        pass

    @abstractmethod
    def getAngle(self) -> float:
        pass
    
class Polar2DAdapter(IVector, IPolar2D):

    def __init__(self, vector: "Vector2D") -> None:
        self.srcVector = vector

    def abs(self) -> float:
        return self.srcVector.abs()

    def cdot(self, vector) -> float:
        return self.srcVector.cdot(vector)

    def getAngle(self) -> float:
        return degrees(atan2(self.srcVector.y, self.srcVector.x))

    def getComponents(self) -> list[float]:
        return self.srcVector.getComponents()
    
    def getX(self) -> float:
        return self.srcVector.getX()

    def getY(self) -> float:
        return self.srcVector.getY()
    

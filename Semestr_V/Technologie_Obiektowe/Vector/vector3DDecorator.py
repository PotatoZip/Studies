from vector2D import IVector, Vector2D
from typing import List
import math

class Vector3DDecorator(Vector2D):
    def __init__(self, x, y, z = 0) -> None:
        self.scrVector = Vector2D(x,y)
        self.z = z
    
    def abs(self) -> float:
        return math.sqrt((self.scrVector.abs()*self.scrVector.abs()) + (self.getZ()*self.getZ()))

    def cdot(self, vector: 'IVector') -> float:
        if (hasattr(vector, "getZ")):
            return self.scrVector.cdot(vector) + self.getZ()*vector.getZ()
        else:
            return self.scrVector.cdot(vector) + self.getZ()*0

    def getComponents(self) -> list[float]:
        return [self.scrVector.getX(), self.scrVector.getY(), self.getZ()]
    
    def getPolars(self) -> list[float]:
        return [round(self.abs(), 2), round(math.atan2(self.scrVector.getY(), self.scrVector.getX()), 2), round(math.acos(self.z/self.abs()), 2)]
    
    def cross(self, vector) -> 'Vector3DDecorator':
        if (hasattr(vector, "getZ")):
            x = self.scrVector.getY()*vector.getZ() - self.getZ()*vector.getY()
            y = self.getZ()*vector.getX() - self.scrVector.getX()*vector.getZ()
            z = self.scrVector.getX()*vector.getY() - self.scrVector.getY()*vector.getX()
        else:
            x = -self.getZ()*vector.getY()
            y = self.getZ()*vector.getX() 
            z = self.scrVector.getX()*vector.getY() - self.scrVector.getY()*vector.getX()
        return Vector3DDecorator(x, y, z)
    
    def getX(self) -> float:
        return self.scrVector.getX()
    
    def getY(self) -> float:
        return self.scrVector.getY()
    
    def getZ(self) -> float:
        return self.z

    def getSrcV(self) -> Vector2D:
        return self.scrVector
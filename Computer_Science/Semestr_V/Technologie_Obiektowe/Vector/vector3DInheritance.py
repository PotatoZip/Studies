from vector2D import Vector2D, IVector
from typing import List
import math

class Vector3DInheritance(Vector2D):
    def __init__(self, x, y, z):
        super().__init__(x, y)
        self.z = z
    
    def abs(self) -> float:
        return math.sqrt((super().abs()*super().abs()) + (self.z*self.z))

    def cdot(self, vector: 'Vector2D') -> float:
        if (hasattr(vector, "getZ")):
            return super().cdot(vector) + self.getZ()*vector.getZ()
        else:
            return super().cdot(vector) + self.getZ()*0

    def getComponents(self) -> list[float]:
        return [self.getX(), self.getY(), self.getZ()]
    
    def getPolars(self) -> list[float]:
        return [round(self.abs(), 2), round(math.atan2(self.getY(), self.getX()), 2), round(math.acos(self.z/self.abs()), 2)]

    def cross(self, vector: 'Vector2D'):
        if (hasattr(vector, "getZ")):
            x = self.getY()*vector.getZ() - self.z*vector.getY()
            y = self.getZ()*vector.getX() - self.getX()*vector.getZ()
            z = self.getX()*vector.getY() - self.getY()*vector.getX()
        else:
            x = -self.z*vector.getY()
            y = self.z*vector.getX() 
            z = self.getX()*vector.getY() - self.getY()*vector.getX()
        return Vector3DInheritance(x, y, z)

    def getSrcV(self) -> Vector2D:
        return Vector2D(self.getX(), self.getY())
    
    def getZ(self) -> float:
        return self.z
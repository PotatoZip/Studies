from vector2D import IVector, Vector2D
from typing import List
from math import atan2, degrees

class Polarinheritance2D(Vector2D):

    def __init__(self, x, y) -> None:
        super().__init__(x,y)

    def getAngle(self) -> float:
        return degrees(atan2(self.x, self.y))
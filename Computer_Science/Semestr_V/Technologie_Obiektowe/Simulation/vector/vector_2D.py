from .i_vector import IVector


class Vector2D(IVector):
    def __init__(self, x : float, y : float) -> None:
        self.x = x
        self.y = y
        
    def get_components(self) -> list[float]:
        return [self.get_x(), self.get_y()]
    
    def abs(self) -> float:
        return (self.get_x()**2 + self.get_y()**2)**0.5
    
    def cdot(self, other: 'Vector2D') -> float:
        return self.get_x()*other.get_x() + self.get_y()*other.get_y()
    
    def get_x(self) -> float:
        return self.x
    
    def get_y(self) -> float:
        return self.y
    
    def set_x(self, x: float):
        self.x = x
        
    def set_y(self, y: float):
        self.y = y
    
    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        return Vector2D(self.get_x() + other.get_x(), self.get_y() + other.get_y())
    
    def distance(self, other: 'Vector2D') -> float:
        return ((self.get_x() - other.get_x())**2 + (self.get_y() - other.get_y())**2)**0.5


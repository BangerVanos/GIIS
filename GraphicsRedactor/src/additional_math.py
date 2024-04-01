from dataclasses import dataclass
from math import sqrt
from numbers import Number


@dataclass
class Point:
    x: int | float
    y: int | float

    @property
    def coords(self) -> tuple:
        return (self.x, self.y)
    
    def scalar_multiply(self, coeff):
        if not isinstance(coeff, Number):
            raise TypeError(f'{coeff} is not a numeric type!')
        return Point(coeff * self.x, coeff * self.y)
    
    def __mul__(self, other):
        if isinstance(other, Number):
            return Point(self.x * other, self.y * other)
        elif isinstance(other, Point):
            return Point(self.x * other.x, self.y * other.y)
        else:
            raise TypeError(f'{other} is not a numeric or Point type!')
    
    def __truediv__(self, other):
        if isinstance(other, Number):
            return Point(self.x / other, self.y / other)
        elif isinstance(other, Point):
            return Point(self.x / other.x, self.y / other.y)
        else:
            raise TypeError(f'{other} is not a numeric or Point type!')
    
    def __add__(self, other):
        if not isinstance(self, Point):
            raise TypeError(f'Can only add two points, but not point and ' 
                            f'{type(other)}')
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        if not isinstance(self, Point):
            raise TypeError(f'Can only subtract two points, but not point and ' 
                            f'{type(other)}')
        return Point(self.x - other.x, self.y - other.y)
    
    def distance(self, other) -> float:
        if not isinstance(other, Point):
            raise TypeError('Can measure distance only between points!\n'
                            f'Other object type is {type(other)}')
        return sqrt(abs(self.x - other.x)**2 + abs(self.y - other.y)**2)


@dataclass
class Pixel:
    point: Point
    color: str
    alpha: int

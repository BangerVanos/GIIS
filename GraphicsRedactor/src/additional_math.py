from dataclasses import dataclass
from math import sqrt


@dataclass
class Point:
    x: int | float
    y: int | float

    @property
    def coords(self) -> tuple:
        return (self.x, self.y)
    
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

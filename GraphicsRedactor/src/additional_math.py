from dataclasses import dataclass


@dataclass
class Point:
    x: int | float
    y: int | float

    @property
    def coords(self) -> tuple:
        return (self.x, self.y)

@dataclass
class Pixel:
    point: Point
    color: str
    alpha: int

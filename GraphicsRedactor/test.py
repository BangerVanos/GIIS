from src.additional_math import Point, Pixel
from src.clipping.clipping import Clipping2D


print(Clipping2D.clipping([Point(5, 5), Point(7, 7),
                           Point(7, 9), Point(11, 4),
                           Point(1, 5), Point(4, 1),
                           Point(10, 8), Point(4, 4)],
                           '#111111', 255))

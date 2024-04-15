from enum import IntEnum
from additional_math import Point, Pixel
from typing import Iterable


class RegionCodes(IntEnum):
    INSIDE = 0
    LEFT = 1
    RIGHT = 2
    BOTTOM = 4
    TOP = 8


class Clipping2D:

    @classmethod
    def clipping(cls, c_points: list[Point], color: str = '#000000',
                 alpha: int = 255) -> list[Pixel]:
        b_points = (c_points.pop(-1), c_points.pop(-1))
        edges = ((c_points[i], c_points[(i+1)%len(c_points)])
                 for i in range(len(c_points)))
        accepted_points = [a_edge := cls._line_clip(edge[0], edge[1])
                           for edge in edges if a_edge is not None]
    
    @classmethod
    def _find_boundary_four(cls, b_points: Iterable[Point]):
        '''Finding boundary rectangle corner points
        coordinates'''
        x_min = min([bpt.x for bpt in b_points])
        y_min = min([bpt.y for bpt in b_points])
        x_max = max([bpt.x for bpt in b_points])
        y_max = max([bpt.y for bpt in b_points])

        return (x_min, y_min, x_max, y_max)
        
    
    @classmethod
    def _pt_region_code(cls, p: Point, b_points: Iterable[Point]) -> int:
        x_min, y_min, x_max, y_max = cls._find_boundary_four(b_points)        

        code = RegionCodes.INSIDE
        if p.x < x_min:
            code |= RegionCodes.LEFT
        elif p.x > x_max:
            code |= RegionCodes.RIGHT
        if p.y < y_min:
            code |= RegionCodes.BOTTOM
        elif p.y > y_max:
            code |= RegionCodes.TOP
        return code
    
    @classmethod
    def _line_clip(cls, p1: Point, p2: Point, b_points: Iterable[Point]):
        x_min, y_min, x_max, y_max = cls._find_boundary_four(b_points)
        x1, y1, x2, y2 = p1.x, p1.y, p2.x, p2.y

        code1 = cls._pt_region_code(p1, b_points)
        code2 = cls._pt_region_code(p2, b_points)
        accept = False

        while True:

            if code1 == 0 and code2 == 0:
                accept = True
                break
            elif (code1 & code2) != 0:
                break
            else:
                x = 1
                y = 1
                if code1 != 0:
                    code_out = code1
                else:
                    code_out = code2
                
                if code_out & RegionCodes.TOP:
                    x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                    y = y_max
                elif code_out & RegionCodes.BOTTOM:
                    x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                    y = y_min
                elif code_out & RegionCodes.RIGHT:
                    y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                    x = x_max
                elif code_out & RegionCodes.LEFT:
                    y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                    x = x_min
                
                if code_out == code1:
                    x1 = x
                    y1 = y
                    code1 = cls._pt_region_code(Point(x1, y1), b_points)
                else:
                    x2 = x
                    y2 = y
                    code2 = cls._pt_region_code(Point(x2, y2), b_points)
        
        if accept:
            return (Point(x1, y1), Point(x2, y2))
        else:
            return None


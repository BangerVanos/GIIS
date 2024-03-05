from PIL import Image as img
import numpy as np
from src.additional_math import Point, Pixel


class FirstOrderLine:
    
    @staticmethod
    def dda(start: Point, end: Point, color: str = '#000000') -> list[Pixel]:
        dx = end.x - start.x
        dy = end.y - start.y
        steps_amount = abs(dx) if abs(dx) > abs(dy) else abs(dy)
        dx /= steps_amount
        dy /= steps_amount
        x, y = start.x, start.y
        px_list = []
        for _ in range(steps_amount):
            px_list.append(
                Pixel(Point(round(x), round(y)), color, 255)
            )
            x += dx
            y += dy
        return px_list

    @staticmethod
    def bresenham(start: Point, end: Point, color: str = '#000000') -> list[Pixel]:
        dx = abs(end.x - start.x)
        sx = 1 if start.x < end.x else -1
        dy = -abs(end.y - start.y)
        sy = 1 if start.y < end.y else -1
        err = dx + dy
        px_list = []
        x, y = start.x, start.y
        while True:
            px_list.append(
                Pixel(Point(round(x), round(y)), color)
            )
            if x == end.x and y == end.y:
                break
            err2 = err * 2
            if err2 >= dy:
                if x == end.x:
                    break
                err += dy
                x += sx
            if err2 <= dx:
                if y == end.y:
                    break
                err += dx
                y += sy
        return px_list

    @staticmethod
    def wu(start: Point, end: Point) -> list:
        pass

    @staticmethod
    def gupta_sproull(start: Point, end: Point) -> list:
        pass

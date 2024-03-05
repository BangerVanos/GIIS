from PIL import Image as img
import numpy as np
from src.additional_math import Point, Pixel
from math import sqrt


class FirstOrderLine:
    
    @staticmethod
    def dda(start: Point, end: Point, color: str = '#000000', alpha: int = 255) -> list[Pixel]:
        dx = end.x - start.x
        dy = end.y - start.y
        steps_amount = abs(dx) if abs(dx) > abs(dy) else abs(dy)
        dx /= steps_amount
        dy /= steps_amount
        x, y = start.x, start.y
        px_list = []
        for _ in range(steps_amount):
            px_list.append(
                Pixel(Point(round(x), round(y)), color, alpha)
            )
            x += dx
            y += dy
        return px_list

    @staticmethod
    def bresenham(start: Point, end: Point, color: str = '#000000', alpha: int = 255) -> list[Pixel]:
        dx = abs(end.x - start.x)
        sx = 1 if start.x < end.x else -1
        dy = -abs(end.y - start.y)
        sy = 1 if start.y < end.y else -1
        err = dx + dy
        px_list = []
        x, y = start.x, start.y
        while True:
            px_list.append(
                Pixel(Point(round(x), round(y)), color, alpha)
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
    def wu(start: Point, end: Point, color: str = '#000000', alpha: int = 255) -> list[Pixel]:

        if start == end:
            return [
                Pixel(Point(start.x, start.y), color, alpha)
            ]

        fpart = lambda x: x - int(x)
        rfpart = lambda x: 1 - fpart(x)        

        x1, y1 = start.x, start.y
        x2, y2 = end.x, end.y

        dx, dy = x2 - x1, y2 - y1
        steep = abs(dx) < abs(dy)

        p = lambda px, py: ((px, py), (py, px))[steep]

        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
            dx, dy = dy, dx
        if x2 < x1:
            x1, x2 = x2, x1

        grad = dy / dx
        intery = y1 + rfpart(x1) * grad

        px_list = []

        def add_endpoint(pt):
            x, y = pt
            xend = round(x)
            yend = y + grad * (xend - x)
            xgap = rfpart(x + 0.5)
            px, py = int(xend), int(yend)
            px_list.append(
                Pixel(Point(*p(px, py)), color, int(rfpart(yend) * xgap * 255))
            )
            px_list.append(
                Pixel(Point(*p(px, py+1)), color, int(fpart(yend) * xgap * 255))
            )
            return px

        xstart = add_endpoint(p(start.x, start.y)) + 1
        xend = add_endpoint(p(end.x, end.y))

        for x in range(xstart, xend, 1 if xstart <= xend else -1):
            y = int(intery)
            px_list.append(
                Pixel(Point(*p(x, y)), color, int(abs(rfpart(intery) * 255)))
            )
            px_list.append(
                Pixel(Point(*p(x, y+1)), color, int(abs(fpart(intery) * 255)))
            )
            intery += grad       
        
        return px_list

    @staticmethod
    def gupta_sproull(start: Point, end: Point, color: str = '#000000', alpha: int = 255) -> list:

        if start == end:
            return [
                Pixel(Point(start.x, start.y), color, alpha)
            ]

        x = start.x
        y = start.y

        dx = end.x - start.x
        dy = end.y - start.y

        sx = 1 if start.x < end.x else -1
        sy = 1 if start.y < end.y else -1

        d = 2 * dy - dx

        euc_point = 0
        length = sqrt(dx**2 + dy**2)

        sin = dx / length
        cos = dy / length

        px_list: list[Pixel] = []
        while(x != end.x):
            px_list.append(
                Pixel(Point(round(x), round(y) - 1),
                      color, int(255 - abs(euc_point + cos) // 2))
            )
            px_list.append(
                Pixel(Point(round(x), round(y)),
                      color, int(255 - abs(euc_point) // 2))
            )
            px_list.append(
                Pixel(Point(round(x), round(y) + 1),
                      color, int(255 - abs(euc_point - cos) // 2))
            )
            
            x += sx
            if d <= 0:
                euc_point += sin
                d += d * dy
            else:
                euc_point += sin - cos
                d += 2 * (dy - dx)
                y += sy
                             
        return px_list

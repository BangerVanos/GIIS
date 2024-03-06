from PIL import Image as img
import numpy as np
from src.additional_math import Point, Pixel
from math import ceil


class SecondOrderLine:

    @classmethod
    def circumference(cls, center: Point, outside: Point, color: str = '#000000',
               alpha: int = 255):
        '''Bresenhams circumference drawing algorithm'''
        px_list: list[Pixel] = []

        def put_circumference_pixels(center: Point, iter: Point):
            px_list.extend(
                [
                    Pixel(Point(center.x + iter.x, center.y + iter.y), color, alpha),
                    Pixel(Point(center.x - iter.x, center.y + iter.y), color, alpha),
                    Pixel(Point(center.x + iter.x, center.y - iter.y), color, alpha),
                    Pixel(Point(center.x - iter.x, center.y - iter.y), color, alpha),
                    Pixel(Point(center.x + iter.y, center.y + iter.x), color, alpha),
                    Pixel(Point(center.x - iter.y, center.y + iter.x), color, alpha),
                    Pixel(Point(center.x + iter.y, center.y - iter.x), color, alpha),
                    Pixel(Point(center.x - iter.y, center.y - iter.x), color, alpha)
                ]
            )
        radius = int(center.distance(outside))
        x, y = 0, radius
        d = 3 - 2 * radius
        while y >= x:            
            if d > 0:
                y -= 1
                d += 4 * (x - y) + 10
            else:
                d += 4 * x + 6
            put_circumference_pixels(center, Point(x, y))
            x += 1
        return px_list

    @classmethod
    def ellipse(cls, center: Point, outside: Point, color: str = '#000000',
                alpha: int = 255):
        
        px_list: list[Pixel] = []
        
        x0, x1 = center.x, outside.x
        y0, y1 = center.y, outside.y

        a = int(abs(x0 - x1))
        b = int(abs(y0 - y1))

        b1 = b & 1
        dx = 4*(1-a)*b**2
        dy = 4*(b1+1)*a**2

        err = dx + dy + b1*a**2

        if x0 > x1:
            x0 = x1
            x1 += a
        if y0 > y1:
            y0 = y1
        y0 += (b + 1) // 2
        y1 = y0 - b1

        a *= 8 * a
        b1 = 8 * b**2

        while x0 <= x1:
            px_list.extend(
                [
                    Pixel(Point(x0, y0), color, alpha),
                    Pixel(Point(x0, y1), color, alpha),
                    Pixel(Point(x1, y0), color, alpha),
                    Pixel(Point(x1, y1), color, alpha)
                ]
            )
            err2 = 2 * err
            if err2 <= dy:
                y0 += 1
                y1 -= 1
                dy += a
                err += dy
            if err2 >= dx and err2 > dy:
                x0 += 1
                x1 -= 1
                dx += b1
                err += dx
        
        while y0 - y1 < b:
            px_list.extend(
                [
                    Pixel(Point(x0 - 1, y0), color, alpha),
                    Pixel(Point(x0 - 1, y1), color, alpha),
                    Pixel(Point(x1 + 1, y0 := y0 + 1), color, alpha),
                    Pixel(Point(x1 + 1, y1 := y1 - 1), color, alpha)
                ]
            )
        return px_list
    
    @classmethod
    def hyperbola(cls, center: Point, ab: Point, end: Point,
                  color: str = '#000000', alpha: int = 255) -> list[Pixel]:
        a = ab.x - center.x
        b = ab.y - center.y

        px_list: list[Pixel] = []

        def put_hyperbola_pixels(center: Point, iter: Point):
            px_list.extend(
                [
                    Pixel(Point(center.x + iter.x, center.y + iter.y), color, alpha),
                    Pixel(Point(center.x - iter.x, center.y + iter.y), color, alpha),
                    Pixel(Point(center.x + iter.x, center.y - iter.y), color, alpha),
                    Pixel(Point(center.x - iter.x, center.y - iter.y), color, alpha)
                ]
            )
    
        x, y = a, 0
        d = 2*a**2-2*a*b-b**2         
        while y <= (int(b**2*x / (a**2)) + 1):
            put_hyperbola_pixels(center, Point(x, y))
            if d < 0:
                d += 2 * a**2 * (2 * y + 3)
            else:
                d += 2 * a**2 * (2 * y + 3) - 4 * b**2 * (x + 1)
                x += 1
            y += 1
        iters = int(ab.distance(end))        
        while iters := iters - 1:
            put_hyperbola_pixels(center, Point(x, y))
            if d < 0:
                d += 2 * b**2 * (3 + 2 * x)
            else:
                d += 2 * b**2 * (3 + 2 * x) - 4 * a**2 * (y + 1)
                y += 1
            x += 1            
        return px_list

    @classmethod
    def parabola(cls, center: Point, ab: Point,
                 color: str = '#000000', alpha: int = 255) -> list[Pixel]:
        a = abs(ab.x - center.x)
        d = 4 - 8 * a
        x, y = 0, 0

        sx = np.sign(ab.x - center.x)
        sy = np.sign(ab.y - center.y)

        px_list: list[Pixel] = []

        def put_parabola_pixels(center: Point, iter: Point):
            px_list.extend(
                [
                    Pixel(Point(center.x + iter.x, center.y + iter.y), color, alpha),
                    Pixel(Point(center.x + iter.x, center.y - iter.y), color, alpha)
                ]
            )
        
        y_stop = 2 * a
        y_d = y
        
        for _ in range(y_stop):
            put_parabola_pixels(center, Point(x, y))
            if d < 0:
                d += 2* (6 + 4 * y_d)
            else:
                d += 2 * (6 + 4 * y_d - 4 * a)
                x += sx
                
            y += sy
            y_d += 1
        d = 1 - 8 * a

        x_stop = 2 * a
        for _ in range(x_stop):
            put_parabola_pixels(center, Point(x, y))
            if d > 0:
                d += -16 * a
            else:
                d += 4 * (2 + 2 * y_d - 4 * a)
                y += sy
                y_d += 1
            x += sx
        return px_list

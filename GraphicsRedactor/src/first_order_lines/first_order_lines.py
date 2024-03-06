from PIL import Image as img
import numpy as np
from src.additional_math import Point, Pixel
from math import sqrt, floor


class FirstOrderLine:
    
    @staticmethod
    def dda(start: Point, end: Point, color: str = '#000000', alpha: int = 255) -> list[Pixel]:

        if start == end:
            return [
                Pixel(Point(start.x, start.y), color, alpha)
            ]

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

        p = lambda px, py: ((px, py), (py, px))[int(steep)]

        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
            dx, dy = dy, dx
        if x2 < x1:
            x1, x2 = x2, x1
            y1, y2 = y2, y1                                                        

        grad = 1 if dx == 0 else dy / dx
         
        intery = y1 + rfpart(x1) * grad

        px_list = []

        def add_endpoint(pt):
            x, y = pt
            xend = round(x)
            yend = y + grad * (xend - x)
            xgap = rfpart(x + 0.5)
            px, py = int(xend), int(floor(yend))
            px_list.append(
                Pixel(Point(*p(px, py)), color, int(abs(rfpart(yend) * xgap * alpha)))
            )
            px_list.append(
                Pixel(Point(*p(px, py+1)), color, int(abs(fpart(yend) * xgap * alpha)))
            )
            return px

        xstart = add_endpoint((x1, y1)) + 1
        xend = add_endpoint((x2, y2))
        print(xstart, xend)                

        for x in range(xstart, xend):
            y = int(intery)
            px_list.append(
                Pixel(Point(*p(x, y)), color, int(abs(rfpart(intery) * alpha)))
            )
            px_list.append(
                Pixel(Point(*p(x, y+1)), color, int(abs(fpart(intery) * alpha)))
            )
            intery += grad      
        
        return px_list

    @staticmethod
    def gupta_sproull(start: Point, end: Point, color: str = '#000000', alpha: int = 255) -> list:

        def count_alpha(distance):
            return int(alpha * (1 - pow(distance * 2 / 3, 2)))

        if start == end:
            return [
                Pixel(Point(start.x, start.y), color, alpha)
            ]

        x = start.x
        y = start.y

        dx = end.x - start.x
        dy = end.y - start.y

        adx = abs(dx)
        ady = abs(dy)

        if adx > ady:
            du = adx
            dv = ady
            u = end.x
        else:
            du = ady
            dv = adx
            u = end.y
        
        sx = 1 if dx > 0 else -1
        sy = 1 if dy > 0 else -1

        u_end = u + du
        d = 2 * dv - du
        incrS = 2 * dv
        incrD = 2 * (dv - du)

        two_vdu = 0
        invD = 1 / (2 * sqrt(du**2 + dv**2))
        invD2u = 2 * du * invD       

        px_list: list[Pixel] = []

        # For better performance, this condition was put forward (even assuming that such code
        # is 30% bigger)
        if adx > ady:

            while u < u_end:
                px_list.append(
                    Pixel(Point(round(x), round(y)),
                        color, count_alpha(two_vdu * invD))
                )
                px_list.append(
                    Pixel(Point(round(x), round(y) + sy),
                        color, count_alpha(invD2u - two_vdu * invD))
                )
                px_list.append(
                    Pixel(Point(round(x), round(y) - sy),
                        color, count_alpha(invD2u + two_vdu * invD))
                )

                if d <= 0:
                    two_vdu = d + du
                    d += incrS
                else:
                    two_vdu = d - du
                    d += incrD
                    y += sy
                u += 1
                x += sx
        
        else:

            while u < u_end:
                px_list.append(
                    Pixel(Point(round(x), round(y)),
                        color, count_alpha(two_vdu * invD))
                )
                px_list.append(
                    Pixel(Point(round(x) + sx, round(y)),
                        color, count_alpha(invD2u - two_vdu * invD))
                )
                px_list.append(
                    Pixel(Point(round(x) - sx, round(y)),
                        color, count_alpha(invD2u + two_vdu * invD))
                )

                if d <= 0:
                    two_vdu = d + du
                    d += incrS
                else:
                    two_vdu = d - du
                    d += incrD
                    x += sx
                u += 1
                y += sy        
                             
        return px_list
